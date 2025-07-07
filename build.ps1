# PowerShell script to build HarImageExtractor.exe

$scriptPath = Split-Path -Parent $MyInvocation.MyCommand.Path
$source = Join-Path $scriptPath "extractor_modified.py"

if (-Not (Test-Path $source)) {
    Write-Error "Файл extractor_modified.py не найден!"
    exit 1
}

pyinstaller `
    --onefile `
    --noconsole `
    --name HarImageExtractor `
    $source
