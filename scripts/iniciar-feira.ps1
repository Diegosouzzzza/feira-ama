# Preparação para o dia da feira: confere o ambiente, explica o que falta e, se puder, sobe o
# serviço e abre o navegador. Nunca liga a esteira sozinho: isso só acontece quando alguém
# clica em Iniciar na tela de Operação.
param([switch]$SemNavegador)
. "$PSScriptRoot\_ambiente.ps1"
Assert-Comando uv 'Instale com: python -m pip install --user uv'

$Script:avisos = @()
$Script:bloqueios = @()
function Escrever-Ok([string]$msg) { Write-Host "  [ok]      $msg" -ForegroundColor Green }
function Escrever-Aviso([string]$msg) { Write-Host "  [atenção] $msg" -ForegroundColor Yellow; $Script:avisos += $msg }
function Escrever-Falta([string]$msg) { Write-Host "  [falta]   $msg" -ForegroundColor Red; $Script:bloqueios += $msg }

Write-Host "`nAmazonVision 4.0 — conferência antes de abrir`n" -ForegroundColor Cyan

# ---------------------------------------------------------------- interface compilada
$dist = Join-Path $Raiz 'web\dist\index.html'
$distOk = Test-Path $dist
if ($distOk) {
    Escrever-Ok 'Interface compilada (web\dist)'
}
elseif (Get-Command pnpm -ErrorAction SilentlyContinue) {
    Write-Host '  Compilando a interface (web\dist não existe)...'
    Push-Location (Join-Path $Raiz 'web')
    try {
        pnpm install --frozen-lockfile
        pnpm build
        $distOk = Test-Path $dist
    } finally { Pop-Location }
    if ($distOk) { Escrever-Ok 'Interface compilada agora' } else { Escrever-Falta 'Falha ao compilar a interface.' }
}
else {
    Escrever-Falta 'Interface não compilada e o pnpm não está instalado. Rode "pnpm build" em web\ antes da feira, num notebook com Node.'
}

# ---------------------------------------------------------------- configuração (api\.env)
$envPath = Join-Path $Raiz 'api\.env'
$config = @{}
if (Test-Path $envPath) {
    Get-Content $envPath | Where-Object { $_ -match '^\s*[A-Za-z_][A-Za-z0-9_]*\s*=' } | ForEach-Object {
        $partes = $_ -split '=', 2
        $config[$partes[0].Trim()] = $partes[1].Trim()
    }
}
$modo = if ($config.AV_MODE) { $config.AV_MODE } else { 'simulado' }
Escrever-Ok "Modo configurado: $modo"
if ($modo -ne 'real') {
    Escrever-Aviso 'Modo simulado: a bancada não vai usar a placa, a câmera nem o modelo reais. Para a feira, defina AV_MODE=real em api\.env.'
}

# ---------------------------------------------------------------- placa e câmera (modo real)
if ($modo -eq 'real') {
    $portaConfigurada = $config.AV_SERIAL_PORT
    $portasDisponiveis = @([System.IO.Ports.SerialPort]::GetPortNames())
    if (-not $portaConfigurada) {
        Escrever-Falta 'AV_SERIAL_PORT não está em api\.env: a bancada não vai falar com a placa.'
    }
    elseif ($portasDisponiveis -contains $portaConfigurada) {
        Escrever-Ok "Placa: porta $portaConfigurada disponível"
    }
    else {
        $lista = if ($portasDisponiveis.Count) { $portasDisponiveis -join ', ' } else { 'nenhuma porta USB encontrada' }
        Escrever-Falta "Placa: porta $portaConfigurada não encontrada ($lista). Confira o cabo USB e o driver (CH340/CP210x)."
    }

    if ($config.AV_CAMERA_SOURCE) {
        Escrever-Ok "Câmera configurada (AV_CAMERA_SOURCE=$($config.AV_CAMERA_SOURCE))"
    }
    else {
        Escrever-Falta 'AV_CAMERA_SOURCE não está em api\.env: a bancada não vai enxergar as peças.'
    }
}

# ---------------------------------------------------------------- integridade dos modelos
$dadosBase = Join-Path $env:LOCALAPPDATA "AmazonVision\$modo"
$pastaModelos = Join-Path $dadosBase 'models'
if (Test-Path $pastaModelos) {
    $pacotes = @(Get-ChildItem $pastaModelos -Directory -ErrorAction SilentlyContinue)
    $integros = 0
    $corrompidos = @()
    foreach ($pacote in $pacotes) {
        $manifesto = Join-Path $pacote.FullName 'model.json'
        $pesos = Join-Path $pacote.FullName 'model.onnx'
        if ((Test-Path $manifesto) -and (Test-Path $pesos)) {
            try {
                $dados = Get-Content $manifesto -Raw | ConvertFrom-Json
                $hash = (Get-FileHash $pesos -Algorithm SHA256).Hash.ToLower()
                if ($hash -eq $dados.weights_sha256) { $integros++ } else { $corrompidos += $pacote.Name }
            } catch { $corrompidos += $pacote.Name }
        }
        else { $corrompidos += $pacote.Name }
    }
    if ($pacotes.Count -eq 0) {
        Escrever-Aviso 'Nenhum modelo instalado ainda. Instale os pacotes treinados na tela Modelos antes da feira.'
    }
    elseif ($corrompidos.Count -gt 0) {
        Escrever-Falta "Modelo(s) corrompido(s) ou incompleto(s): $($corrompidos -join ', '). A API também recusa carregá-los."
    }
    else {
        Escrever-Ok "$integros modelo(s) instalado(s): pesos conferem com o manifesto"
    }
}
else {
    Escrever-Aviso 'Nenhum modelo instalado ainda (a pasta de modelos não existe).'
}

# ---------------------------------------------------------------- espaço em disco
$unidade = (Get-Item $Raiz).PSDrive.Name
$disco = Get-PSDrive $unidade -ErrorAction SilentlyContinue
if ($disco) {
    $livresGb = [math]::Round($disco.Free / 1GB, 1)
    if ($disco.Free -lt 2GB) {
        Escrever-Falta "Só $livresGb GB livres no disco $unidade`: . Libere espaço (fotos antigas, lixeira) antes de começar."
    }
    elseif ($disco.Free -lt 5GB) {
        Escrever-Aviso "$livresGb GB livres no disco $unidade`: . Deve dar, mas vale apagar fotos antigas."
    }
    else {
        Escrever-Ok "$livresGb GB livres no disco $unidade`:"
    }
}

# ---------------------------------------------------------------- resumo
Write-Host ''
if ($Script:bloqueios.Count -gt 0) {
    Write-Host 'Falta resolver antes de operar com peças reais:' -ForegroundColor Red
    $Script:bloqueios | ForEach-Object { Write-Host "  - $_" -ForegroundColor Red }
    Write-Host ''
}
if ($Script:avisos.Count -gt 0) {
    Write-Host 'Avisos:' -ForegroundColor Yellow
    $Script:avisos | ForEach-Object { Write-Host "  - $_" -ForegroundColor Yellow }
    Write-Host ''
}
if (-not $distOk) {
    Write-Host 'Não dá para abrir sem a interface compilada. Resolva o item acima e rode de novo.' -ForegroundColor Red
    exit 1
}

Write-Host 'Abrindo o serviço local (a esteira só liga quando alguém clicar em Iniciar na tela)...' -ForegroundColor Cyan
Push-Location (Join-Path $Raiz 'api')
try {
    $servico = Start-Process -FilePath 'uv' -ArgumentList 'run', '--no-dev', 'amazonvision' -NoNewWindow -PassThru
    if (-not $SemNavegador) {
        for ($i = 0; $i -lt 40; $i++) {
            Start-Sleep -Milliseconds 500
            try {
                $resposta = Invoke-WebRequest -Uri 'http://127.0.0.1:8000/api/health' -UseBasicParsing -TimeoutSec 1
                if ($resposta.StatusCode -eq 200) { break }
            } catch { }
        }
        Start-Process 'http://127.0.0.1:8000'
    }
    Wait-Process -Id $servico.Id
}
finally {
    Pop-Location
    if ($servico -and -not $servico.HasExited) {
        # uv inicia o Python como processo filho; encerra a árvore inteira.
        taskkill /PID $servico.Id /T /F | Out-Null
    }
}
