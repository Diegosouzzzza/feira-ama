# Bancada real: do firmware gravado à esteira rodando

Passo a passo para sair do modo simulado e operar com o ESP32 DevKit V1, a esteira e um celular como câmera. Os comandos são para o Windows PowerShell, a partir da pasta `amazonvision`.

Pinagem e driver do motor: `docs/firmware.md`. Operação no dia: `docs/feira.md` e `docs/guia-operador.md`.

## 0. Antes de energizar

- Buck LM2596 ajustado em **5,0 V** (medir com multímetro antes de ligar ao VIN do ESP32).
- Alimentação dos atuadores (Motor TT 3–6 V, servo MG996R) separada da lógica, com o **GND em comum**.
- E-STOP solto: o GPIO 27 precisa ler LOW (contato NF fechado ao GND). Com o fio solto a placa entra em `ESTOP` — é o comportamento à prova de falha.
- Nada sobre os sensores S1 e S2.

## 1. Gravar o firmware

Conecte o ESP32 pelo cabo USB e descubra a porta:

```powershell
[System.IO.Ports.SerialPort]::GetPortNames()
```

Grave (troque `COM5` pela sua porta; se houver só uma placa, o `--upload-port` é opcional):

```powershell
cd firmware
& "$env:USERPROFILE\.platformio\penv\Scripts\pio.exe" run -t upload --upload-port COM5
```

Se a gravação parar em `Connecting....`, segure o botão **BOOT** da placa até começar a escrever.

Confira que a placa está viva (deve aparecer uma linha `"type":"hb"` por segundo; saia com `Ctrl+C`):

```powershell
& "$env:USERPROFILE\.platformio\penv\Scripts\pio.exe" device monitor --port COM5 --baud 115200
cd ..
```

**Feche o monitor antes de continuar**: só um programa por vez abre a porta COM.

## 2. Ligar o celular como câmera

Escolha um dos modos. Pelo cabo USB é mais estável que por Wi-Fi.

### a) Webcam virtual (DroidCam ou Iriun)

1. Instale o app no celular e o cliente no Windows; conecte (USB ou Wi-Fi) e deixe a imagem aparecendo no cliente.
2. O celular vira mais uma câmera do Windows. Descubra o índice:

   ```powershell
   .\scripts\listar-cameras.ps1 -Abrir
   ```

   O script salva uma foto de cada câmera em `%LOCALAPPDATA%\AmazonVision\cameras` (`camera-0.jpg`, `camera-1.jpg`...) e abre a pasta. Em geral `0` é a webcam do notebook e o celular é `1` ou `2`. Se a foto for o logotipo do app, o celular não está conectado.
3. Use o índice: `AV_CAMERA_SOURCE=1`.

### b) Stream pelo cabo USB (IP Webcam + adb)

1. No celular: ative a **depuração USB** e, no app IP Webcam, toque em **Iniciar servidor** (porta 8080).
2. No Windows (precisa do `adb`, do pacote *platform-tools* do Android):

   ```powershell
   adb devices
   adb forward tcp:8080 tcp:8080
   ```

3. Teste: `.\scripts\listar-cameras.ps1 -Url http://127.0.0.1:8080/video -Abrir`
4. Use `AV_CAMERA_SOURCE=http://127.0.0.1:8080/video`.

O `adb forward` **se perde quando o cabo é desconectado**: rode de novo depois de reconectar.

### c) Stream por Wi-Fi

Use o endereço que o app mostra, com celular e notebook na mesma rede: `AV_CAMERA_SOURCE=http://192.168.0.50:8080/video` (IP Webcam) ou `http://192.168.0.50:4747/video` (DroidCam). Também aceita `rtsp://`.

### Ajustes de imagem

- **Imagem deitada**: `AV_CAMERA_ROTATE=90` (ou `180`, `270`), sentido horário. Vale para a inspeção, a coleta e a visualização ao vivo. Teste com `.\scripts\listar-cameras.ps1 -Girar 90`.
- **Foco, exposição e balanço de branco**: no modo stream são ajustados **no app do celular** — trave-os lá (foco e exposição fixos), senão o modelo aprende variações de iluminação. `AV_CAMERA_WIDTH/HEIGHT/EXPOSURE` só valem para câmera por índice.
- **"A câmera não entregou uma imagem nova" (`STALE_FRAME`)**: o stream atrasou. Aumente `AV_CAMERA_CAPTURE_TIMEOUT_S` (padrão 2,0 s), mantendo-o bem abaixo do "Prazo da decisão" do produto na tela Configuração.
- Se o app do celular cair, a API desiste da leitura em 5 s e tenta reabrir o stream a cada segundo, sozinha.
- **Mudou a rotação ou a câmera depois de coletar fotos?** O dataset e a região de inspeção (ROI) foram feitos na orientação antiga: refaça-os.

## 3. Configurar `api\.env`

```powershell
Copy-Item api\.env.example api\.env    # só na primeira vez
notepad api\.env
```

Mínimo para a bancada real (exemplo com IP Webcam pelo cabo):

```ini
AV_MODE=real
AV_SERIAL_PORT=COM5
AV_CAMERA_SOURCE=http://127.0.0.1:8080/video
AV_CAMERA_ROTATE=0
```

O modo real usa um banco de dados próprio (`%LOCALAPPDATA%\AmazonVision\real`), separado do simulado: produtos calibrados, modelos e lotes do simulado não aparecem nele.

## 4. Subir

```powershell
.\scripts\iniciar-feira.ps1 -SemQuiosque
```

O script confere a interface compilada, a porta serial, a câmera (para stream, se o endereço responde), os modelos e o disco, e só então sobe o serviço e abre o navegador. Sem `-SemQuiosque` abre o Modo feira em tela cheia.

Conferência, com o serviço no ar:

| O que | Onde | Esperado |
|---|---|---|
| Placa | tela **Diagnóstico**, ou `http://127.0.0.1:8000/api/status` | conectada, firmware `0.2.0`, estado `DISARMED` |
| Portas | `http://127.0.0.1:8000/api/diagnostics/serial-ports` | a porta configurada com `in_use: true` |
| Câmera | `http://127.0.0.1:8000/api/camera/snapshot` | a imagem da esteira, na orientação certa |
| Outras câmeras | `http://127.0.0.1:8000/api/diagnostics/cameras` | lista dos índices, com `snapshot_url` de cada um |

## 5. Primeiro movimento

1. Tela **Configuração**: calibre o produto (tempos, ângulos do servo e, se quiser a esteira mais lenta, "Potência do motor" — vazio é potência total).
2. Tela **Diagnóstico → Manutenção**: teste o motor (1 s) e o servo (repouso e rejeição). O relé K1 só fecha em manutenção ou armada, com o E-STOP solto.
3. Passe a mão em S1 e S2 e veja os sensores mudarem na tela.
4. Aperte o E-STOP: LED vermelho, buzzer e estado `ESTOP`. Solte e use **Rearmar**.
5. Abra um lote e clique em **Iniciar**.

## Se algo der errado

| Sintoma | Causa provável | O que fazer |
|---|---|---|
| "A placa não está respondendo" logo ao subir | A placa reiniciou ao abrir a porta e ainda está subindo | Aguarde 2–3 s: a API refaz o `HELLO` no primeiro *heartbeat*. Se persistir, confira `AV_SERIAL_PORT` e feche o monitor serial. |
| "não foi possível abrir COM5" no log | Porta em uso (monitor do PlatformIO, Arduino IDE) ou cabo solto | Feche o outro programa; a API tenta reabrir a cada 2 s. |
| Estado `ESTOP` sem o botão apertado | Contato NF aberto ou fio do GPIO 27 solto | Conferir a fiação: o normal é o GPIO 27 em LOW. |
| Câmera `unavailable` | Stream fora do ar, `adb forward` perdido, índice errado, câmera em uso por outro programa | `.\scripts\listar-cameras.ps1` (com o serviço parado). |
| Câmera `stale` | O celular parou de mandar quadros (tela bloqueou, app em segundo plano) | Deixar o app em primeiro plano, com a tela ligada e o celular na tomada. |
| Motor não gira em potência baixa | Abaixo do torque de partida do Motor TT | Aumentar "Potência do motor" (comece em 60–70 %). |
| Velocidade não muda com a potência, ou MOSFET quente | Optoacoplador do módulo D4184 lento para 20 kHz | Recompilar com `-DAV_MOTOR_PWM_HZ=2000` (ver `docs/firmware.md`). |
| Servo treme quando o motor liga | Queda de tensão na alimentação dos atuadores | Capacitor eletrolítico (≥ 470 µF) junto ao servo; conferir bitola e GND comum. |
