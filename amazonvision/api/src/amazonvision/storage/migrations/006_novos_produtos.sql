-- 006: adiciona Pupunha e Taperebá como produtos iniciais do sistema.
INSERT OR IGNORE INTO product_profiles (id, name, presentation, decision_threshold, created_at, updated_at) VALUES
    ('pupunha',  'Pupunha',  NULL, 0.80, strftime('%Y-%m-%dT%H:%M:%fZ', 'now'), strftime('%Y-%m-%dT%H:%M:%fZ', 'now')),
    ('tapereba', 'Taperebá', NULL, 0.80, strftime('%Y-%m-%dT%H:%M:%fZ', 'now'), strftime('%Y-%m-%dT%H:%M:%fZ', 'now'));
