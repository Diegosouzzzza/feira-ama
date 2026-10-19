# Confere as ferramentas de desenvolvimento e mostra o que falta.
. "$PSScriptRoot\_ambiente.ps1"
$ErrorActionPreference = 'Continue'

$itens = @(
    @{ Nome = 'git';    Args = '--version'; Dica = 'https://git-scm.com' },
    @{ Nome = 'python'; Args = '--version'; Dica = 'Python 3.12 (python.org)' },
    @{ Nome = 'uv';     Args = '--version'; Dica = 'python -m pip install --user uv' },
    @{ Nome = 'node';   Args = '--version'; Dica = 'Node 22+ (só desenvolvimento do web/)' },
    @{ Nome = 'pnpm';   Args = '--version'; Dica = 'npm install -g pnpm' },
    @{ Nome = 'pio';    Args = '--version'; Dica = 'uv tool install platformio' }
)

$faltando = 0
foreach ($i in $itens) {
    if (Get-Command $i.Nome -ErrorAction SilentlyContinue) {
        $versao = (& $i.Nome $i.Args 2>$null | Select-Object -First 1)
        Write-Host ("[ok]    {0,-7} {1}" -f $i.Nome, $versao) -ForegroundColor Green
    } else {
        $faltando++
        Write-Host ("[falta] {0,-7} -> {1}" -f $i.Nome, $i.Dica) -ForegroundColor Yellow
    }
}

$py = (python --version 2>$null)
if ($py -and $py -notmatch '3\.12\.') { Write-Host "[aviso] O projeto usa Python 3.12; encontrado: $py" -ForegroundColor Yellow }

if ($faltando -eq 0) { Write-Host "`nAmbiente completo." -ForegroundColor Green } else { exit 1 }
