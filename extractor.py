# CLI tool for extracting base64 images from a HAR file
# Консольная утилита для извлечения base64-изображений из HAR-файла

import json
import os
import base64
from tkinter import filedialog
from tkinter import Tk

# Disable main Tkinter window (we only need the file dialogs)
# Отключаем главное окно Tkinter (нужны только диалоги)
Tk().withdraw()

# Ask user to select a HAR file
# Запрашиваем у пользователя .har-файл
har_path = filedialog.askopenfilename(
    title="Select HAR file",
    filetypes=[("HAR files", "*.har")]
)

# Exit if no file selected
# Выход, если файл не выбран
if not har_path:
    print("No HAR file selected. Exiting.")
    exit()

# Ask user to select output folder (optional)
# Запрос папки сохранения (опционально)
output_folder = filedialog.askdirectory(title="Select output folder (Cancel = auto)")

if not output_folder:
    # Create folder from HAR filename if user cancels
    # Если отмена — создаём папку по имени HAR-файла
    har_name = os.path.splitext(os.path.basename(har_path))[0]
    output_folder = os.path.join("output", har_name)

# Ensure the folder exists
# Убеждаемся, что папка существует
os.makedirs(output_folder, exist_ok=True)

# Load HAR file as JSON
# Загружаем HAR-файл как JSON
with open(har_path, "r", encoding="utf-8") as f:
    har_data = json.load(f)

# Get entries from HAR structure
# Получаем список запросов из HAR
entries = har_data.get("log", {}).get("entries", [])
image_count = 0

# Iterate over all HTTP entries
# Проходим по каждому HTTP-запросу
for entry in entries:
    response = entry.get("response", {})
    content = response.get("content", {})
    mime_type = content.get("mimeType", "")

    # Check if the response is an image with base64 encoding
    # Проверяем, что это изображение с кодировкой base64
    if mime_type.startswith("image/") and "base64" in content.get("encoding", ""):
        ext = mime_type.split("/")[-1]  # e.g., png, jpeg, webp
        raw_data = base64.b64decode(content.get("text", ""))
        filename = f"image_{image_count:03d}.{ext}"
        filepath = os.path.join(output_folder, filename)

        # Write image to file
        # Сохраняем изображение в файл
        with open(filepath, "wb") as img_file:
            img_file.write(raw_data)
            image_count += 1

# Print result
# Выводим результат
print(f"✅ Extracted {image_count} image(s) to '{output_folder}/'")
