-- 002: dados do pacote de modelo usados na ativação e na auditoria.
ALTER TABLE model_versions ADD COLUMN recommended_threshold REAL
    CHECK (recommended_threshold IS NULL OR (recommended_threshold > 0 AND recommended_threshold <= 1));
ALTER TABLE model_versions ADD COLUMN validated_by TEXT;
ALTER TABLE model_versions ADD COLUMN validated_at TEXT;
