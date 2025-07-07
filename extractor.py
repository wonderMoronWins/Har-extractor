
import json
import os
import base64

def extract_images(har_path, output_folder):
    # Ensure subfolder 'img' exists
    output_folder = os.path.join(output_folder, 'img')
    os.makedirs(output_folder, exist_ok=True)

    with open(har_path, 'r', encoding='utf-8') as f:
        har_data = json.load(f)

    entries = har_data.get('log', {}).get('entries', [])
    image_count = 0

    for entry in entries:
        response = entry.get('response', {})
        content = response.get('content', {})
        mime_type = content.get('mimeType', '')
        if mime_type.startswith('image/') and 'base64' in content.get('encoding', ''):
            ext = mime_type.split('/')[-1]
            raw_data = base64.b64decode(content.get('text', ''))
            filename = f"image_{image_count:03d}.{ext}"
            filepath = os.path.join(output_folder, filename)
            with open(filepath, 'wb') as img_file:
                img_file.write(raw_data)
            image_count += 1

    return image_count


if __name__ == "__main__":
    from tkinter import filedialog, Tk
    Tk().withdraw()
    har = filedialog.askopenfilename(
        title="Select HAR file",
        filetypes=[("HAR files", "*.har")]
    )
    if not har:
        exit()
    folder = filedialog.askdirectory(title="Select output folder")
    if not folder:
        exit()
    count = extract_images(har, folder)
    print(f"✅ Extracted {count} images to '{os.path.join(folder, 'img')}/'")
