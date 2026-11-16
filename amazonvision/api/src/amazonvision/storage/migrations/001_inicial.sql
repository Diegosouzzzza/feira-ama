-- 001: esquema inicial do AmazonVision 4.0
-- Horários: texto ISO-8601 em UTC terminado em Z (exibição em America/Manaus é papel da interface).
-- O executor envolve este arquivo em uma transação: não use BEGIN/COMMIT aqui.

-- ---------------------------------------------------------------- perfis e modelos

CREATE TABLE product_profiles (
    id                  TEXT PRIMARY KEY
                        CHECK (length(id) BETWEEN 2 AND 32 AND id NOT GLOB '*[^a-z0-9_]*' AND id GLOB '[a-z]*'),
    name                TEXT NOT NULL CHECK (length(name) BETWEEN 1 AND 60),
    presentation        TEXT,
    decision_threshold  REAL NOT NULL CHECK (decision_threshold > 0 AND decision_threshold <= 1),
    active_model_id     TEXT,
    bench_config_json   TEXT CHECK (bench_config_json IS NULL OR json_valid(bench_config_json)),
    version             INTEGER NOT NULL DEFAULT 1 CHECK (version >= 1),
    created_at          TEXT NOT NULL CHECK (created_at GLOB '[0-9][0-9][0-9][0-9]-[0-9][0-9]-[0-9][0-9]T[0-9][0-9]:[0-9][0-9]:[0-9][0-9]*Z'),
    updated_at          TEXT NOT NULL CHECK (updated_at GLOB '[0-9][0-9][0-9][0-9]-[0-9][0-9]-[0-9][0-9]T[0-9][0-9]:[0-9][0-9]:[0-9][0-9]*Z'),
    FOREIGN KEY (id, active_model_id) REFERENCES model_versions (product_id, id)
) STRICT;

CREATE TABLE model_versions (
    id                  TEXT PRIMARY KEY CHECK (length(id) BETWEEN 1 AND 64),
    product_id          TEXT NOT NULL REFERENCES product_profiles (id),
    architecture        TEXT NOT NULL,
    weights_path        TEXT NOT NULL,
    weights_sha256      TEXT NOT NULL CHECK (length(weights_sha256) = 64 AND weights_sha256 NOT GLOB '*[^0-9a-f]*'),
    class_order_json    TEXT NOT NULL CHECK (json_valid(class_order_json)),
    preprocess_json     TEXT NOT NULL CHECK (json_valid(preprocess_json)),
    dataset_version     TEXT NOT NULL,
    metrics_json        TEXT CHECK (metrics_json IS NULL OR json_valid(metrics_json)),
    validation_status   TEXT NOT NULL DEFAULT 'pending' CHECK (validation_status IN ('pending', 'validated', 'rejected')),
    created_at          TEXT NOT NULL CHECK (created_at GLOB '[0-9][0-9][0-9][0-9]-[0-9][0-9]-[0-9][0-9]T[0-9][0-9]:[0-9][0-9]:[0-9][0-9]*Z'),
    UNIQUE (product_id, id)
) STRICT;

-- ---------------------------------------------------------------- lotes, sessões e ciclos

CREATE TABLE lots (
    id                    INTEGER PRIMARY KEY,
    request_id            TEXT NOT NULL UNIQUE,
    product_id            TEXT NOT NULL REFERENCES product_profiles (id),
    model_id              TEXT,
    operator              TEXT NOT NULL CHECK (length(operator) BETWEEN 1 AND 60),
    status                TEXT NOT NULL DEFAULT 'open' CHECK (status IN ('open', 'closed')),
    is_simulated          INTEGER NOT NULL CHECK (is_simulated IN (0, 1)),
    policy_threshold      REAL NOT NULL CHECK (policy_threshold > 0 AND policy_threshold <= 1),
    policy_version        TEXT NOT NULL,
    config_snapshot_json  TEXT NOT NULL CHECK (json_valid(config_snapshot_json)),
    notes                 TEXT CHECK (notes IS NULL OR length(notes) <= 500),
    started_at            TEXT NOT NULL CHECK (started_at GLOB '[0-9][0-9][0-9][0-9]-[0-9][0-9]-[0-9][0-9]T[0-9][0-9]:[0-9][0-9]:[0-9][0-9]*Z'),
    ended_at              TEXT CHECK (ended_at IS NULL OR ended_at GLOB '[0-9][0-9][0-9][0-9]-[0-9][0-9]-[0-9][0-9]T[0-9][0-9]:[0-9][0-9]:[0-9][0-9]*Z'),
    CHECK ((status = 'open') = (ended_at IS NULL)),
    FOREIGN KEY (product_id, model_id) REFERENCES model_versions (product_id, id)
) STRICT;

-- No máximo um lote aberto por vez.
CREATE UNIQUE INDEX lots_one_open ON lots (status) WHERE status = 'open';

CREATE TABLE device_sessions (
    id                INTEGER PRIMARY KEY,
    boot_id           TEXT NOT NULL CHECK (length(boot_id) = 8 AND boot_id NOT GLOB '*[^0-9a-f]*'),
    session_id        TEXT NOT NULL CHECK (length(session_id) = 8 AND session_id NOT GLOB '*[^0-9a-f]*'),
    firmware_version  TEXT,
    protocol_version  INTEGER NOT NULL,
    port              TEXT,
    opened_at         TEXT NOT NULL CHECK (opened_at GLOB '[0-9][0-9][0-9][0-9]-[0-9][0-9]-[0-9][0-9]T[0-9][0-9]:[0-9][0-9]:[0-9][0-9]*Z'),
    closed_at         TEXT CHECK (closed_at IS NULL OR closed_at GLOB '[0-9][0-9][0-9][0-9]-[0-9][0-9]-[0-9][0-9]T[0-9][0-9]:[0-9][0-9]:[0-9][0-9]*Z'),
    UNIQUE (boot_id, session_id)
) STRICT;

CREATE TABLE cycles (
    id                     INTEGER PRIMARY KEY,
    lot_id                 INTEGER NOT NULL REFERENCES lots (id),
    seq_in_lot             INTEGER NOT NULL CHECK (seq_in_lot >= 1),
    device_session_id      INTEGER REFERENCES device_sessions (id),
    status                 TEXT NOT NULL DEFAULT 'running' CHECK (status IN ('running', 'completed', 'aborted')),
    commanded_destination  TEXT CHECK (commanded_destination IN ('APPROVED', 'REJECTED')),
    abort_reason           TEXT,
    started_at             TEXT NOT NULL CHECK (started_at GLOB '[0-9][0-9][0-9][0-9]-[0-9][0-9]-[0-9][0-9]T[0-9][0-9]:[0-9][0-9]:[0-9][0-9]*Z'),
    ended_at               TEXT CHECK (ended_at IS NULL OR ended_at GLOB '[0-9][0-9][0-9][0-9]-[0-9][0-9]-[0-9][0-9]T[0-9][0-9]:[0-9][0-9]:[0-9][0-9]*Z'),
    UNIQUE (lot_id, seq_in_lot),
    CHECK ((status = 'running') = (ended_at IS NULL)),
    CHECK (status <> 'aborted' OR abort_reason IS NOT NULL),
    CHECK (status <> 'completed' OR commanded_destination IS NOT NULL)
) STRICT;

-- Uma peça por vez na bancada.
CREATE UNIQUE INDEX cycles_one_running ON cycles (status) WHERE status = 'running';

-- ---------------------------------------------------------------- inspeções e revisões

CREATE TABLE inspections (
    id                INTEGER PRIMARY KEY,
    cycle_id          INTEGER NOT NULL UNIQUE REFERENCES cycles (id),
    image_path        TEXT NOT NULL UNIQUE,
    image_sha256      TEXT NOT NULL CHECK (length(image_sha256) = 64 AND image_sha256 NOT GLOB '*[^0-9a-f]*'),
    image_purged_at   TEXT,
    captured_at       TEXT NOT NULL CHECK (captured_at GLOB '[0-9][0-9][0-9][0-9]-[0-9][0-9]-[0-9][0-9]T[0-9][0-9]:[0-9][0-9]:[0-9][0-9]*Z'),
    frame_age_ms      REAL CHECK (frame_age_ms IS NULL OR frame_age_ms >= 0),
    model_id          TEXT REFERENCES model_versions (id),
    predicted_grade   TEXT CHECK (predicted_grade IN ('A', 'B', 'C')),
    scores_json       TEXT CHECK (scores_json IS NULL OR json_valid(scores_json)),
    confidence        REAL CHECK (confidence IS NULL OR (confidence >= 0 AND confidence <= 1)),
    latency_ms        REAL CHECK (latency_ms IS NULL OR latency_ms >= 0),
    policy_threshold  REAL NOT NULL CHECK (policy_threshold > 0 AND policy_threshold <= 1),
    policy_version    TEXT NOT NULL,
    auto_decision     TEXT NOT NULL CHECK (auto_decision IN ('APPROVED', 'REJECTED', 'REVIEW')),
    review_reason     TEXT CHECK (review_reason IN ('LOW_CONFIDENCE', 'AMBIGUOUS', 'INVALID_IMAGE')),
    final_decision    TEXT CHECK (final_decision IN ('APPROVED', 'REJECTED')),
    decided_by        TEXT CHECK (decided_by IN ('auto', 'operator')),
    created_at        TEXT NOT NULL CHECK (created_at GLOB '[0-9][0-9][0-9][0-9]-[0-9][0-9]-[0-9][0-9]T[0-9][0-9]:[0-9][0-9]:[0-9][0-9]*Z'),
    CHECK ((auto_decision = 'REVIEW') = (review_reason IS NOT NULL)),
    CHECK ((predicted_grade IS NULL) = (scores_json IS NULL)),
    CHECK ((predicted_grade IS NULL) = (confidence IS NULL)),
    CHECK (review_reason IS NOT 'INVALID_IMAGE' OR predicted_grade IS NULL),
    CHECK ((final_decision IS NULL) = (decided_by IS NULL)),
    CHECK (auto_decision = 'REVIEW' OR final_decision IS NOT NULL)
) STRICT;

CREATE INDEX inspections_captured_at ON inspections (captured_at);

-- A previsão original nunca é alterada; correções entram como revisão.
CREATE TRIGGER inspections_prediction_immutable
BEFORE UPDATE OF cycle_id, image_path, image_sha256, captured_at, model_id, predicted_grade,
                 scores_json, confidence, latency_ms, policy_threshold, policy_version,
                 auto_decision, review_reason
ON inspections
BEGIN
    SELECT RAISE(ABORT, 'previsao original da inspecao e imutavel');
END;

CREATE TRIGGER inspections_no_delete BEFORE DELETE ON inspections
BEGIN
    SELECT RAISE(ABORT, 'inspecoes nao podem ser apagadas');
END;

CREATE TABLE reviews (
    id                 INTEGER PRIMARY KEY,
    inspection_id      INTEGER NOT NULL REFERENCES inspections (id),
    request_id         TEXT NOT NULL UNIQUE,
    reviewer           TEXT NOT NULL CHECK (length(reviewer) BETWEEN 1 AND 60),
    previous_decision  TEXT CHECK (previous_decision IN ('APPROVED', 'REJECTED')),
    new_decision       TEXT NOT NULL CHECK (new_decision IN ('APPROVED', 'REJECTED')),
    reason             TEXT NOT NULL CHECK (length(reason) BETWEEN 3 AND 200),
    created_at         TEXT NOT NULL CHECK (created_at GLOB '[0-9][0-9][0-9][0-9]-[0-9][0-9]-[0-9][0-9]T[0-9][0-9]:[0-9][0-9]:[0-9][0-9]*Z')
) STRICT;

CREATE INDEX reviews_inspection ON reviews (inspection_id);

CREATE TRIGGER reviews_append_only_update BEFORE UPDATE ON reviews
BEGIN
    SELECT RAISE(ABORT, 'revisoes sao somente de acrescimo');
END;

CREATE TRIGGER reviews_append_only_delete BEFORE DELETE ON reviews
BEGIN
    SELECT RAISE(ABORT, 'revisoes sao somente de acrescimo');
END;

-- ---------------------------------------------------------------- eventos

CREATE TABLE events (
    id           INTEGER PRIMARY KEY,
    source       TEXT NOT NULL CHECK (source IN ('device', 'host', 'operator')),
    type         TEXT NOT NULL CHECK (length(type) BETWEEN 1 AND 40),
    severity     TEXT NOT NULL CHECK (severity IN ('info', 'warning', 'error')),
    boot_id      TEXT,
    device_seq   INTEGER CHECK (device_seq IS NULL OR device_seq >= 0),
    lot_id       INTEGER REFERENCES lots (id),
    cycle_id     INTEGER REFERENCES cycles (id),
    data_json    TEXT NOT NULL DEFAULT '{}' CHECK (json_valid(data_json)),
    occurred_at  TEXT NOT NULL CHECK (occurred_at GLOB '[0-9][0-9][0-9][0-9]-[0-9][0-9]-[0-9][0-9]T[0-9][0-9]:[0-9][0-9]:[0-9][0-9]*Z'),
    CHECK ((source = 'device') = (boot_id IS NOT NULL AND device_seq IS NOT NULL)),
    -- Mensagem repetida da placa não é registrada duas vezes.
    UNIQUE (boot_id, device_seq)
) STRICT;

CREATE INDEX events_occurred_at ON events (occurred_at);
CREATE INDEX events_cycle ON events (cycle_id);

-- ---------------------------------------------------------------- dataset (separado da operação)

CREATE TABLE dataset_samples (
    id                   INTEGER PRIMARY KEY,
    product_id           TEXT NOT NULL REFERENCES product_profiles (id),
    physical_sample_id   TEXT NOT NULL CHECK (length(physical_sample_id) BETWEEN 1 AND 40),
    collection_session   TEXT NOT NULL CHECK (length(collection_session) BETWEEN 1 AND 40),
    image_path           TEXT NOT NULL UNIQUE,
    crop_path            TEXT UNIQUE,
    image_sha256         TEXT NOT NULL UNIQUE CHECK (length(image_sha256) = 64 AND image_sha256 NOT GLOB '*[^0-9a-f]*'),
    label                TEXT CHECK (label IN ('A', 'B', 'C')),
    label_author         TEXT,
    status               TEXT NOT NULL DEFAULT 'pending' CHECK (status IN ('pending', 'labeled', 'ambiguous', 'unusable')),
    reviewed_by          TEXT,
    split                TEXT CHECK (split IN ('train', 'val', 'test')),
    dataset_version      TEXT,
    capture_config_json  TEXT CHECK (capture_config_json IS NULL OR json_valid(capture_config_json)),
    created_at           TEXT NOT NULL CHECK (created_at GLOB '[0-9][0-9][0-9][0-9]-[0-9][0-9]-[0-9][0-9]T[0-9][0-9]:[0-9][0-9]:[0-9][0-9]*Z'),
    updated_at           TEXT NOT NULL CHECK (updated_at GLOB '[0-9][0-9][0-9][0-9]-[0-9][0-9]-[0-9][0-9]T[0-9][0-9]:[0-9][0-9]:[0-9][0-9]*Z'),
    CHECK (status <> 'labeled' OR (label IS NOT NULL AND label_author IS NOT NULL)),
    CHECK (split IS NULL OR status = 'labeled')
) STRICT;

CREATE INDEX dataset_samples_physical ON dataset_samples (product_id, physical_sample_id);

-- ---------------------------------------------------------------- resumo derivado dos registros

CREATE VIEW v_lot_summary AS
SELECT
    l.id AS lot_id,
    COUNT(i.id) AS inspected,
    COUNT(CASE WHEN i.final_decision = 'APPROVED' THEN 1 END) AS approved,
    COUNT(CASE WHEN i.final_decision = 'REJECTED' THEN 1 END) AS rejected,
    COUNT(CASE WHEN i.auto_decision = 'REVIEW' AND i.final_decision IS NULL THEN 1 END) AS review_pending,
    COUNT(CASE WHEN i.decided_by = 'operator' THEN 1 END) AS reviewed,
    COUNT(CASE WHEN i.predicted_grade = 'A' THEN 1 END) AS grade_a,
    COUNT(CASE WHEN i.predicted_grade = 'B' THEN 1 END) AS grade_b,
    COUNT(CASE WHEN i.predicted_grade = 'C' THEN 1 END) AS grade_c,
    (SELECT COUNT(*) FROM cycles x WHERE x.lot_id = l.id AND x.status = 'completed') AS cycles_completed,
    (SELECT COUNT(*) FROM cycles x WHERE x.lot_id = l.id AND x.status = 'aborted') AS cycles_aborted
FROM lots l
LEFT JOIN cycles c ON c.lot_id = l.id
LEFT JOIN inspections i ON i.cycle_id = c.id
GROUP BY l.id;

-- ---------------------------------------------------------------- perfis iniciais
-- Limiar provisório: será recalibrado na validação de cada modelo (Bloco 8).

INSERT INTO product_profiles (id, name, presentation, decision_threshold, created_at, updated_at) VALUES
    ('tucuma',   'Tucumã',           NULL, 0.80, strftime('%Y-%m-%dT%H:%M:%fZ', 'now'), strftime('%Y-%m-%dT%H:%M:%fZ', 'now')),
    ('castanha', 'Castanha-do-pará', NULL, 0.80, strftime('%Y-%m-%dT%H:%M:%fZ', 'now'), strftime('%Y-%m-%dT%H:%M:%fZ', 'now'));
