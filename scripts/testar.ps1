# Roda lint, testes e verificação de tipos de todas as partes.
. "$PSScriptRoot\_ambiente.ps1"
# Each step is judged by its exit code; tools that print warnings on stderr must not abort the run.
$ErrorActionPreference = 'Continue'
$falhas = @()

Push-Location (Join-Path $Raiz 'api')
uv run ruff check .;             if ($LASTEXITCODE) { $falhas += 'api: ruff check' }
uv run ruff format --check .;    if ($LASTEXITCODE) { $falhas += 'api: ruff format' }
uv run pytest -q;                if ($LASTEXITCODE) { $falhas += 'api: pytest' }
Pop-Location

Push-Location (Join-Path $Raiz 'web')
pnpm typecheck;                  if ($LASTEXITCODE) { $falhas += 'web: typecheck' }
pnpm test;                       if ($LASTEXITCODE) { $falhas += 'web: vitest' }
pnpm test:e2e;                   if ($LASTEXITCODE) { $falhas += 'web: playwright (Edge)' }
Pop-Location

if (Get-Command pio -ErrorAction SilentlyContinue) {
    Push-Location (Join-Path $Raiz 'firmware')
    pio run;                     if ($LASTEXITCODE) { $falhas += 'firmware: pio run' }
    Pop-Location
}

if ($falhas) { Write-Host "`nFalhas: $($falhas -join ', ')" -ForegroundColor Red; exit 1 }
Write-Host "`nTudo certo." -ForegroundColor Green
