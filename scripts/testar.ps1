# Roda lint, testes e verificação de tipos de todas as partes.
. "$PSScriptRoot\_ambiente.ps1"
# Each step is judged by its exit code; tools that print warnings on stderr must not abort the run.
$ErrorActionPreference = 'Continue'
$falhas = @()

Push-Location (Join-Path $Raiz 'api')
# The training group (PyTorch) is included so the real training test runs too.
uv run --group training ruff check .;           if ($LASTEXITCODE) { $falhas += 'api: ruff check' }
uv run --group training ruff format --check .;  if ($LASTEXITCODE) { $falhas += 'api: ruff format' }
uv run --group training pytest -q;              if ($LASTEXITCODE) { $falhas += 'api: pytest' }
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
