# Carregado pelos outros scripts: garante uv e pio no PATH desta sessão.
$ErrorActionPreference = 'Stop'
$Script:Raiz = Split-Path -Parent $PSScriptRoot

$extras = @(
    (Join-Path $env:APPDATA 'Python\Python312\Scripts'),
    (Join-Path $env:USERPROFILE '.local\bin')
)
foreach ($dir in $extras) {
    if ((Test-Path $dir) -and -not ($env:Path -split ';' -contains $dir)) {
        $env:Path = "$dir;$env:Path"
    }
}

function Assert-Comando([string]$nome, [string]$dica) {
    if (-not (Get-Command $nome -ErrorAction SilentlyContinue)) {
        throw "Comando '$nome' não encontrado. $dica"
    }
}
