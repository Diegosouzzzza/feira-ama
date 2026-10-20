-- 004: teste de concordância na rotulagem. Duas (ou mais) pessoas rotulam as mesmas fotos da
-- coleta sem ver a resposta uma da outra; o resumo é calculado depois, comparando os rótulos.
CREATE TABLE label_agreement (
    id          INTEGER PRIMARY KEY,
    sample_id   INTEGER NOT NULL REFERENCES dataset_samples (id),
    session     TEXT NOT NULL CHECK (length(session) BETWEEN 1 AND 40),
    reviewer    TEXT NOT NULL CHECK (length(reviewer) BETWEEN 1 AND 60),
    label       TEXT NOT NULL CHECK (label IN ('A', 'B', 'C')),
    created_at  TEXT NOT NULL CHECK (created_at GLOB '[0-9][0-9][0-9][0-9]-[0-9][0-9]-[0-9][0-9]T[0-9][0-9]:[0-9][0-9]:[0-9][0-9]*Z'),
    updated_at  TEXT NOT NULL CHECK (updated_at GLOB '[0-9][0-9][0-9][0-9]-[0-9][0-9]-[0-9][0-9]T[0-9][0-9]:[0-9][0-9]:[0-9][0-9]*Z'),
    -- Each reviewer labels a given photo once per session; labeling again updates the answer.
    UNIQUE (sample_id, session, reviewer)
) STRICT;

CREATE INDEX label_agreement_session ON label_agreement (session, sample_id);
