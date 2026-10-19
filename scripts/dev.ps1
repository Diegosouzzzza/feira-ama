# Desenvolvimento: API com recarga automática + Vite com proxy para /api.
# Abra http://127.0.0.1:5173 . Ctrl+C encerra os dois.
. "$PSScriptRoot\_ambiente.ps1"
Assert-Comando uv 'Instale com: python -m pip install --user uv'
Assert-Comando pnpm 'Instale o Node 22+ e o pnpm.'

Push-Location (Join-Path $Raiz 'api')
uv sync | Out-Null
$api = Start-Process -FilePath 'uv' -ArgumentList 'run', 'amazonvision', '--reload' -NoNewWindow -PassThru
Pop-Location

try {
    Push-Location (Join-Path $Raiz 'web')
    if (-not (Test-Path node_modules)) { pnpm install }
    pnpm dev
}
finally {
    Pop-Location
    if ($api -and -not $api.HasExited) {
        # uv inicia o Python como processo filho; encerra a árvore inteira.
        taskkill /PID $api.Id /T /F | Out-Null
    }
}
