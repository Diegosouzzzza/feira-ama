# Execução como na feira: compila o web/ (se preciso) e sobe só a API, que serve a interface.
# Abra http://127.0.0.1:8000
param([switch]$RecompilarWeb)
. "$PSScriptRoot\_ambiente.ps1"
Assert-Comando uv 'Instale com: python -m pip install --user uv'

$dist = Join-Path $Raiz 'web\dist\index.html'
if ($RecompilarWeb -or -not (Test-Path $dist)) {
    Assert-Comando pnpm 'Para compilar a interface é preciso o Node 22+ e o pnpm.'
    Push-Location (Join-Path $Raiz 'web')
    try { pnpm install --frozen-lockfile; pnpm build } finally { Pop-Location }
}

Push-Location (Join-Path $Raiz 'api')
try { uv run --no-dev amazonvision } finally { Pop-Location }
