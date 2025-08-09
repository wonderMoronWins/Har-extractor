import json
import os
import base64

CATEGORY_MAP = {
    "image": "img",
    "application/pdf": "doc",
    "application/msword": "doc",
    "application/vnd": "doc",
    "text/plain": "doc",
    "text/html": "doc",
    "application/xml": "doc",
    "application/javascript": "js",
    "text/javascript": "js",
    "text/css": "css",
    "font/": "font",
    "application/font": "font",
    "application/json": "data",
    "application/octet-stream": "data"
}

def resolve_category(mime_type):
    for key, folder in CATEGORY_MAP.items():
        if key in mime_type:
            return folder
    return "other"

def extract_images(har_path, output_folder):
    with open(har_path, 'r', encoding='utf-8') as f:
        har_data = json.load(f)

    count_map = {}

    for entry in har_data.get("log", {}).get("entries", []):
        content = entry.get("response", {}).get("content", {})
        mime_type = content.get("mimeType", "")
        text = content.get("text", "")
        encoding = content.get("encoding", "")

        if not mime_type or encoding != "base64" or not text:
            continue

        category = resolve_category(mime_type)
        ext = mime_type.split("/")[-1].split(";")[0]
        ext = "jpg" if ext == "jpeg" else ext
        category_path = os.path.join(output_folder, category)
        os.makedirs(category_path, exist_ok=True)

        count = count_map.get(category, 0)
        filename = os.path.join(category_path, f"{category}_{count}.{ext}")
        try:
            raw = base64.b64decode(text)
            with open(filename, "wb") as f:
                f.write(raw)
            count_map[category] = count + 1
        except Exception:
            continue
