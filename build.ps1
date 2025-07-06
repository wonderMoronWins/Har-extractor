# build.ps1 — build script for creating standalone .exe from extractor_gui.py

# Step 1: Clean previous build artifacts
# Шаг 1: Очистка старых файлов сборки
Remove-Item -Recurse -Force build, dist, extractor_gui.spec -ErrorAction SilentlyContinue

# Step 2: Compile extractor_gui.py into one .exe with icon
# Шаг 2: Компиляция GUI-файла в один .exe с иконкой
pyinstaller extractor_gui.py --onefile --noconsole --icon="icon\ihar.ico"

# Step 3: Open the dist folder with the built executable
# Шаг 3: Открытие папки с готовым exe-файлом
Start-Process .\dist
