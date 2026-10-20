# ADR 0014 — Preparação para o dia da feira: inicialização, backup e retenção

Data: 2026-10-20 · Situação: aceita

## Decisões

1. **`scripts/iniciar-feira.ps1`** confere o ambiente (interface compilada, modo, porta serial, câmera, integridade dos modelos por SHA-256, espaço em disco) e explica o que falta, **sem nunca ligar a esteira** — isso só acontece quando alguém clica em Iniciar na tela. As checagens rodam em PowerShell puro (sem precisar do serviço já no ar), incluindo `[System.IO.Ports.SerialPort]::GetPortNames()` para a porta serial.
2. **Backup pela API** (`POST /api/backups`): usa `VACUUM INTO` no mesmo fio de execução que grava o banco, garantindo uma cópia consistente mesmo com o serviço em operação; empacota junto as fotos, os modelos e a coleta num `.zip` em `backups/`, com metadados ao lado (contagens, tamanho) para a listagem. Tentar copiar a pasta de dados por fora com o serviço aberto falha (o SQLite mantém o arquivo em uso no Windows) — por isso o backup pela API é o caminho recomendado durante o dia.
3. **`scripts/backup.ps1`/`restaurar.ps1`** cobrem o cenário sem o serviço rodando (fim do dia, ou uma restauração): o de backup recusa rodar com o serviço no ar; o de restauração exige o serviço parado e sempre guarda os dados atuais ao lado (`…antes-de-restaurar-<data>`) antes de sobrescrever, nunca apaga nada sem essa rede de segurança.
4. **Retenção automática de fotos de inspeção**: `AV_IMAGE_RETENTION_DAYS` (30) e `AV_RETENTION_CHECK_MINUTES` (60) apagam só o arquivo de fotos de lotes **já encerrados**, mantendo a linha no banco (previsão, decisão, eventos, CSV) — a coluna `image_purged_at`, que já existia no esquema desde o Bloco 2 sem nada que a usasse, finalmente tem um dono. O lote aberto nunca é tocado. Também disponível sob demanda (`POST /api/images/purge`) e pela tela Configuração.
5. **`docs/feira.md`** reúne os quatro itens (ligação serial, inicialização, backup/restauração, retenção) e a lista de conferência antes de sair de casa; `docs/guia-operador.md` é a folha de uma página para quem vai operar no dia, sem precisar ler o resto.

## Evidências

- `iniciar-feira.ps1` testado manualmente em modo simulado (tudo ok) e em modo real sem porta/câmera configuradas (bloqueios corretos, sem travar a inicialização do serviço).
- `backup.ps1` recusado com o serviço rodando (reproduzido o erro de arquivo em uso); com o serviço parado, backup e restauração completos testados de ponta a ponta, inclusive subindo o serviço sobre os dados restaurados e conferindo `/api/status`.
- Testes da API: backup com contagens corretas, zip baixável e com um banco íntegro dentro, listagem, exclusão, limpeza respeitando o lote aberto e a idade configurada, recusa sem controle.
