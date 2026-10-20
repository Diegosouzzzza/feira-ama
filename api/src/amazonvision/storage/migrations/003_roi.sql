-- 003: região de inspeção (ROI) por produto. Recorte relativo (0..1) do quadro da câmera,
-- aplicado antes do letterbox, igual no treino e na inferência. Nulo: usa o quadro inteiro.
ALTER TABLE product_profiles ADD COLUMN roi_json TEXT
    CHECK (roi_json IS NULL OR json_valid(roi_json));
