# Dicionário de dados — esquema v1

Fonte de verdade: `api/src/amazonvision/storage/migrations/001_inicial.sql`. Banco SQLite em `%LOCALAPPDATA%\AmazonVision\db\`, modo WAL, `foreign_keys` ligado, tabelas `STRICT`. Versão do esquema em `PRAGMA user_version`; migrações numeradas, cada uma em uma transação (`api/src/amazonvision/storage/migrator.py`).

Horários: texto ISO-8601 em UTC terminado em `Z`, com milissegundos (`2026-10-18T19:04:11.302Z`).

| Tabela | Registra | Regras principais |
|---|---|---|
| `product_profiles` | Perfil de produto: nome, apresentação (com/sem casca), limiar de decisão, modelo ativo, parâmetros da bancada | O modelo ativo precisa ser do mesmo produto. Perfis iniciais: `tucuma`, `castanha` (limiar provisório 0,80) |
| `model_versions` | Modelo treinado: arquitetura, caminho e SHA-256 dos pesos, ordem das classes, pré-processamento, versão do dataset, métricas, situação de validação | `validation_status`: `pending`, `validated`, `rejected` |
| `lots` | Lote de operação: produto, modelo, operador, limiar e versão da política congelados, cópia da configuração usada | **No máximo um lote aberto.** `request_id` único (idempotência). `is_simulated` separa ensaio de operação real |
| `device_sessions` | Cada conexão com a placa (`boot_id` + `session_id`), firmware e porta | Par `boot_id`/`session_id` único |
| `cycles` | Uma peça na bancada: estado, destino comandado, motivo de interrupção | **No máximo um ciclo em andamento.** Ciclo concluído exige destino; interrompido exige motivo |
| `inspections` | Imagem, previsão A/B/C, scores, confiança, latência, decisão automática e decisão final | Uma por ciclo. **Previsão original imutável** (trigger). Não pode ser apagada. Inconclusivo (`REVIEW`) exige motivo; decisão automática exige decisão final |
| `reviews` | Revisão humana: decisão anterior, nova decisão, responsável, justificativa | Somente acréscimo (sem UPDATE/DELETE). `request_id` único |
| `events` | Linha do tempo: placa, serviço e operador | `(boot_id, device_seq)` único: mensagem repetida da placa não entra duas vezes |
| `dataset_samples` | Amostras de treinamento (separadas da operação): amostra física, sessão de coleta, rótulo, autor, partição | Rotulada exige rótulo e autor; partição só para rotuladas; imagem e hash únicos |

## Visão `v_lot_summary`

Contadores por lote calculados a partir dos registros: `inspected`, `approved`, `rejected` (pela decisão **final**), `review_pending`, `reviewed`, `grade_a/b/c` (pela **previsão** do modelo), `cycles_completed`, `cycles_aborted`. A taxa de aprovação é `approved / (approved + rejected)`, calculada na API, e é nula com denominador zero.

## Fora do banco

- Imagens: arquivos em `%LOCALAPPDATA%\AmazonVision\images\`, referenciados por caminho + SHA-256. O registro só aponta para o arquivo depois que ele foi gravado por completo.
- Pesos dos modelos: `%LOCALAPPDATA%\AmazonVision\models\`, verificados pelo SHA-256.
