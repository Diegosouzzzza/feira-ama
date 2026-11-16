-- 005: regiões geométricas fora do padrão detectadas por modelo de anomalia.
-- Guardadas em frações (0..1) do quadro completo da câmera. Nulo quando o modelo não exporta mapa espacial.
ALTER TABLE inspections ADD COLUMN anomaly_regions_json TEXT
    CHECK (anomaly_regions_json IS NULL OR json_valid(anomaly_regions_json));
