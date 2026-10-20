# Restaura uma cópia feita por backup.ps1 ou baixada da tela Configuração > Backups.
# O serviço precisa estar parado: ele mantém o banco e os arquivos abertos o tempo todo.
param(
    [Parameter(Mandatory)][string]$Arquivo,
    [ValidateSet('simulado', 'real')][string]$Modo = 'real',
    [switch]$Confirmar
)
. "$PSScriptRoot\_ambiente.ps1"
if (-not (Test-Path $Arquivo)) { throw "Arquivo não encontrado: $Arquivo" }

$rodando = $false
try {
    $resposta = Invoke-WebRequest -Uri 'http://127.0.0.1:8000/api/health' -UseBasicParsing -TimeoutSec 1
    $rodando = $resposta.StatusCode -eq 200
} catch { $rodando = $false }
if ($rodando) {
    throw 'O serviço está rodando em 127.0.0.1:8000. Feche-o antes de restaurar (Ctrl+C na janela do serviço) e rode este script de novo.'
}

$destino = Join-Path $env:LOCALAPPDATA "AmazonVision\$Modo"
if (-not $Confirmar) {
    Write-Host "Isto substitui os dados em $destino pelo conteúdo de $Arquivo." -ForegroundColor Yellow
    Write-Host 'Nada foi alterado ainda. Rode de novo com -Confirmar para seguir.' -ForegroundColor Yellow
    exit 1
}

if (Test-Path $destino) {
    $comBackupNome = "$(Split-Path $destino -Leaf).antes-de-restaurar-$(Get-Date -Format 'yyyyMMdd-HHmmss')"
    Write-Host "Guardando os dados atuais como $comBackupNome (por segurança, não apagados)..."
    Rename-Item -Path $destino -NewName $comBackupNome
}

New-Item -ItemType Directory -Path $destino -Force | Out-Null
Write-Host "Extraindo $Arquivo em $destino..."
Expand-Archive -Path $Arquivo -DestinationPath $destino -Force

Write-Host "Pronto. Rode scripts\iniciar.ps1 ou scripts\iniciar-feira.ps1 para conferir." -ForegroundColor Green
