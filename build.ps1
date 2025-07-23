# build.ps1 — сборка HarExtractor.exe одной командой

# Перейти в папку скрипта
Set-Location -Path $PSScriptRoot

# Убедиться, что установлен pyinstaller
if (-not (Get-Command pyinstaller -ErrorAction SilentlyContinue)) {
    Write-Host "PyInstaller не найден. Устанавливаю..."
    pip install pyinstaller
}

# Очистить старые сборки
Remove-Item -Recurse -Force dist, build -ErrorAction SilentlyContinue
Remove-Item HarExtractor.spec -ErrorAction SilentlyContinue

# Выполнить сборку
pyinstaller main.py `
  --onefile `
  --noconsole `
  --name HarExtractor `
  --icon=icon/ihar.ico `
  --distpath dist `
  --workpath build `
  --specpath . `
  --add-data "assets;assets" `
  --add-data "locale;locale" `
  --add-data "config;config" `
  --add-data "src;src"

# Удалить .spec после сборки
Remove-Item HarExtractor.spec -ErrorAction SilentlyContinue

Write-Host "\n✅ Сборка завершена. Файл: dist/HarExtractor.exe"
