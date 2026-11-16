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

# PlatformIO instalado pelo instalador oficial fica em %USERPROFILE%\.platformio\penv. Tem
# prioridade sobre um "pio" do PATH, que pode ser um atalho quebrado de instalação antiga.
# (Só o pio: a pasta inteira no PATH esconderia o python do sistema.)
$pioPenv = Join-Path $env:USERPROFILE '.platformio\penv\Scripts\pio.exe'
if (Test-Path $pioPenv) { Set-Alias -Name pio -Value $pioPenv }

function Assert-Comando([string]$nome, [string]$dica) {
    if (-not (Get-Command $nome -ErrorAction SilentlyContinue)) {
        throw "Comando '$nome' não encontrado. $dica"
    }
}
