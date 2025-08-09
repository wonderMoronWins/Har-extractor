
import os
import json
import base64
import mimetypes

# English: Extract images from HAR file and save them to output folder
# Русский: Извлекает изображения из HAR-файла и сохраняет в папку

def extract_images(har_path, output_folder, progress_callback=None) -> int:
    with open(har_path, "rb") as f:
        raw = f.read()

    text = raw.decode("utf-8", errors="replace")
    data = json.loads(text)

    entries = data.get("log", {}).get("entries", [])
    total = len(entries)
    extracted = 0

    img_dir = os.path.join(output_folder, "img")
    os.makedirs(img_dir, exist_ok=True)

    for i, entry in enumerate(entries):
        mime = entry.get("response", {}).get("content", {}).get("mimeType", "")
        if mime.startswith("image/"):
            content = entry["response"]["content"].get("text")
            if content and entry["response"]["content"].get("encoding") == "base64":
                ext = mimetypes.guess_extension(mime) or ".img"
                path = os.path.join(img_dir, f"image_{i}{ext}")
                try:
                    with open(path, "wb") as img_file:
                        img_file.write(base64.b64decode(content))
                    extracted += 1
                except Exception as e:
                    print(f"Error writing file {path}: {e}")
        if progress_callback:
            progress_callback(int((i + 1) / total * 100))

    return extracted
