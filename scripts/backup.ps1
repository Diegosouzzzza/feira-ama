# Copia a pasta de dados (banco, fotos, modelos, coleta) para um destino, ex.: um pendrive.
# Com o serviço rodando, use a tela Configuração > Backups em vez deste script: ela gera o zip
# pelo próprio serviço, com o banco num instantâneo coerente, sem precisar parar nada. Este
# script é para levar tudo embora no fim do dia, com o serviço já parado.
param(
    [Parameter(Mandatory)][string]$Destino,
    [ValidateSet('simulado', 'real')][string]$Modo = 'real'
)
. "$PSScriptRoot\_ambiente.ps1"

$origem = Join-Path $env:LOCALAPPDATA "AmazonVision\$Modo"
if (-not (Test-Path $origem)) { throw "Nenhum dado encontrado em $origem." }

$rodando = $false
try {
    $resposta = Invoke-WebRequest -Uri 'http://127.0.0.1:8000/api/health' -UseBasicParsing -TimeoutSec 1
    $rodando = $resposta.StatusCode -eq 200
} catch { $rodando = $false }
if ($rodando) {
    throw 'O serviço está rodando em 127.0.0.1:8000 e mantém o banco aberto (a cópia falharia no meio). Pare o serviço (Ctrl+C na janela dele) e rode de novo, ou use a tela Configuração > Backups sem parar nada.'
}

if (-not (Test-Path $Destino)) { New-Item -ItemType Directory -Path $Destino -Force | Out-Null }
$carimbo = Get-Date -Format 'yyyyMMdd-HHmmss'
$arquivo = Join-Path $Destino "amazonvision-$Modo-$carimbo.zip"

# A pasta backups\ fica de fora: são cópias já compactadas, incluí-las engordaria cada backup
# novo com todos os backups antigos.
$itens = @(Get-ChildItem -Path $origem | Where-Object { $_.Name -ne 'backups' })
if (-not $itens) { throw "Pasta de dados vazia em $origem." }

Write-Host "Copiando $origem para $arquivo..."
Compress-Archive -Path $itens.FullName -DestinationPath $arquivo -CompressionLevel Optimal -Force
$tamanhoMb = [math]::Round((Get-Item $arquivo).Length / 1MB, 1)
Write-Host "Pronto: $arquivo ($tamanhoMb MB)" -ForegroundColor Green
