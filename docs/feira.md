# Preparação para o dia da feira

O sistema roda inteiramente local, sem internet (`docs/api.md`, princípio 1). Esta página reúne o que falta conferir antes de abrir: a ligação com a placa, o atalho de inicialização, backup e restauração, e a limpeza automática de fotos antigas.

## Ligação com a placa (modo real)

```
AV_MODE=real
AV_SERIAL_PORT=COM5
AV_SERIAL_BAUD_RATE=115200   # padrão; só muda se o firmware mudar
```

A porta é lida uma vez, na inicialização (igual à câmera, `AV_CAMERA_SOURCE`). Para descobrir qual porta é a placa, a tela **Diagnóstico** mostra as portas USB disponíveis sempre que a placa não está respondendo, com a descrição de cada uma (ex.: "USB-SERIAL CH340").

Se o cabo cair ou a placa reiniciar enquanto o serviço está rodando, a conexão é **reaberta sozinha** a cada poucos segundos, sem precisar reiniciar o serviço; a tela mostra "Placa sem comunicação" enquanto isso. Sem `AV_SERIAL_PORT` configurada, o serviço sobe normalmente, só sem placa (como hoje, antes de a esteira estar montada).

## Abrir no dia: `scripts/iniciar-feira.ps1`

```powershell
.\scripts\iniciar-feira.ps1
```

Confere, nesta ordem, e explica o que falta **sem ligar a esteira** (isso só acontece quando alguém clica em Iniciar na tela):

1. Interface compilada (`web/dist`); compila sozinho se tiver o pnpm à mão.
2. Modo configurado (`AV_MODE`) e, no modo real, a porta serial e a câmera.
3. Modelos instalados: confere o SHA-256 dos pesos de cada um contra o manifesto (pacote corrompido = bloqueio).
4. Espaço livre em disco.

Resolvidos os itens marcados `[falta]`, sobe o serviço e abre o navegador sozinho. `-SemNavegador` pula a abertura automática.

## Backup

Dois jeitos, para situações diferentes:

- **Com o serviço rodando**: tela **Configuração** → **Backups e limpeza** → **Fazer backup agora**. Gera um `.zip` com uma cópia **consistente** do banco (`VACUUM INTO`, no mesmo fio de execução que grava o banco — nunca pega uma escrita pela metade), as fotos de inspeção, os modelos instalados e a coleta de treinamento. Baixe o arquivo e guarde numa unidade separada (pendrive).
- **Com o serviço parado**, para levar tudo embora no fim do dia:
  ```powershell
  .\scripts\backup.ps1 -Destino E:\ -Modo real
  ```
  Copia a pasta de dados inteira para o destino. Recusa rodar com o serviço aberto (o banco fica em uso).

## Restauração

```powershell
.\scripts\restaurar.ps1 -Arquivo E:\amazonvision-real-20261020-180000.zip -Modo real -Confirmar
```

Exige o serviço **parado**. Sem `-Confirmar`, só mostra o que faria. Os dados atuais nunca são apagados: viram `…antes-de-restaurar-<data>` ao lado, por segurança. Depois de restaurar, rode `iniciar.ps1` ou `iniciar-feira.ps1` para conferir.

## Limpeza automática de fotos antigas

As fotos de **inspeção** (não as da Coleta) mais antigas que `AV_IMAGE_RETENTION_DAYS` (padrão 30 dias) e de um **lote já encerrado** são apagadas sozinhas, a cada `AV_RETENTION_CHECK_MINUTES` (padrão 60 min). O registro no banco fica — previsão, decisão, eventos e a linha no CSV continuam lá, só a foto some (a tela mostra "Imagem não está mais disponível"). O lote aberto nunca é tocado, mesmo que esteja com fotos antigas.

Para limpar na hora (por exemplo, véspera da feira, para começar com disco livre): tela **Configuração** → **Backups e limpeza** → **Limpar fotos antigas**, ou:

```
POST /api/images/purge?max_age_days=7
```

## Instalação sem internet

Antes de ir para a feira, com internet disponível:

```powershell
cd api;  uv sync --no-dev
cd ..\web; pnpm install --frozen-lockfile; pnpm build
```

Isso baixa e guarda em cache tudo que os dois precisam (`uv` e `pnpm` reaproveitam o cache local depois, sem internet). Depois, ensaie com o Wi-Fi **desligado**:

1. `scripts\iniciar-feira.ps1` — deve abrir normalmente, sem nenhum aviso de rede.
2. Abra `/api/docs` e `/feira` no navegador: nada deve demorar ou falhar.
3. Rode alguns ciclos (modo simulado ou real) e confira que nada trava esperando a rede.

Se algo falhar sem internet, normalmente é um recurso carregado de fora (fonte, biblioteca): o `web/dist` já embute a fonte Archivo e as bibliotecas da interface, então isso não deve acontecer — mas vale conferir pelo menos uma vez antes do dia.

## Lista antes de sair de casa

- [ ] `AV_MODE=real`, `AV_SERIAL_PORT` e `AV_CAMERA_SOURCE` certos em `api/.env`
- [ ] `iniciar-feira.ps1` sem nenhum `[falta]`
- [ ] Modelos instalados e **validados** pela equipe (tela Modelos)
- [ ] Backup recente testado (gerado e restaurado uma vez, para garantir que funciona)
- [ ] Ensaio com o Wi-Fi desligado
- [ ] Pendrive com o backup e com `web/dist` + o cache do `uv`/`pnpm`, por segurança
