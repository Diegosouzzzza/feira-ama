# Descobre qual câmera é qual (webcam do notebook, webcam virtual do celular, stream) para
# preencher AV_CAMERA_SOURCE em api\.env. Salva uma foto de cada câmera e mostra onde ficaram.
#
#   .\scripts\listar-cameras.ps1                                   # testa os índices 0 a 5
#   .\scripts\listar-cameras.ps1 -Url http://127.0.0.1:8080/video  # testa um stream do celular
#   .\scripts\listar-cameras.ps1 -Girar 90                         # confere a rotação
#
# Feche antes o serviço da bancada (ou outro programa que use a câmera): uma câmera em uso
# por outro programa aparece como "sem imagem".
param(
    [string]$Url,
    [ValidateSet(0, 90, 180, 270)][int]$Girar = 0,
    [int]$Max = 6,
    [switch]$Abrir
)
. "$PSScriptRoot\_ambiente.ps1"
Assert-Comando uv 'Instale com: python -m pip install --user uv'

$pasta = Join-Path $env:LOCALAPPDATA 'AmazonVision\cameras'
$argumentos = @('run', '--no-dev', 'python', '-m', 'amazonvision.camera.probe', '--max', $Max, '--rotate', $Girar, '--out', $pasta)
if ($Url) { $argumentos += @('--url', $Url) }

Push-Location (Join-Path $Raiz 'api')
try {
    $ErrorActionPreference = 'Continue'
    & uv @argumentos
    $codigo = $LASTEXITCODE
} finally { Pop-Location }

if ($Abrir -and (Test-Path $pasta)) { Start-Process $pasta }
exit $codigo
