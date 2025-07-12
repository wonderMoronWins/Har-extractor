# build.ps1 — Сборка HAR Extractor GUI (.exe) с иконкой из папки icon/

$ErrorActionPreference = "Stop"
Write-Host "🚀 Начинаем сборку HAR Extractor..."

# Удаление старых сборок
Remove-Item -Recurse -Force dist, build, *.spec -ErrorAction SilentlyContinue

# Сборка exe с ресурсами, локализацией и иконкой из папки icon/
pyinstaller gui.py `
  --noconfirm `
  --onefile `
  --windowed `
  --clean `
  --icon "icon/ihar.ico" `
  --add-data "assets;assets" `
  --add-data "locale;locale"

# Проверка результата
if (Test-Path "dist\gui.exe") {
    Write-Host "`n✅ Сборка завершена. Файл: dist\gui.exe"
} else {
    Write-Host "`n❌ Ошибка: файл не собран."
}