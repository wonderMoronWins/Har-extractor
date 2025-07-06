# extractor_gui.py — обновлённая версия с улучшенным интерфейсом

import json
import os
import base64
import tkinter as tk
from tkinter import filedialog, messagebox

har_path = ""
output_folder = ""

def select_har():
    global har_path
    har_path = filedialog.askopenfilename(
        title="Select HAR file",
        filetypes=[("HAR files", "*.har")]
    )
    if har_path:
        status_label.config(text=f"Selected: {os.path.basename(har_path)}")

def select_output():
    global output_folder
    output_folder = filedialog.askdirectory(title="Select output folder")
    if output_folder:
        status_label.config(text=f"Output folder selected")

def extract_images():
    if not har_path:
        messagebox.showerror("Error", "No HAR file selected.")
        return
    if not output_folder:
        messagebox.showerror("Error", "No output folder selected.")
        return

    with open(har_path, "r", encoding="utf-8") as f:
        har_data = json.load(f)

    entries = har_data.get("log", {}).get("entries", [])
    image_count = 0

    for entry in entries:
        response = entry.get("response", {})
        content = response.get("content", {})
        mime_type = content.get("mimeType", "")

        if mime_type.startswith("image/") and "base64" in content.get("encoding", ""):
            ext = mime_type.split("/")[-1]
            raw_data = base64.b64decode(content.get("text", ""))
            filename = f"image_{image_count:03d}.{ext}"
            filepath = os.path.join(output_folder, filename)

            with open(filepath, "wb") as img_file:
                img_file.write(raw_data)
                image_count += 1

    # ✔ Добавляем галочку на IMPORT
    import_btn.config(text="✔ IMPORT DONE")
    status_label.config(text=f"Extracted {image_count} image(s)")

# ==== UI ====

window = tk.Tk()
window.title("Import .har")
window.geometry("480x300")
window.configure(bg="#5a7ca7")

title_label = tk.Label(window, text="Import .har", font=("Segoe UI", 18, "bold"), bg="#5a7ca7", fg="white")
title_label.pack(pady=10)

frame = tk.Frame(window, bg="#5a7ca7")
frame.pack(pady=20)

btn1 = tk.Button(frame, text="Select .har file", width=20, command=select_har)
btn1.grid(row=0, column=0, padx=(10, 5))

arrow1 = tk.Label(frame, text="→", font=("Segoe UI", 12), bg="#5a7ca7", fg="white")
arrow1.grid(row=0, column=1)

btn2 = tk.Button(frame, text=".jpg", width=10, state="disabled")
btn2.grid(row=0, column=2, padx=5)

arrow2 = tk.Label(frame, text="→", font=("Segoe UI", 12), bg="#5a7ca7", fg="white")
arrow2.grid(row=0, column=3)

btn3 = tk.Button(frame, text="Select output folder", width=20, command=select_output)
btn3.grid(row=0, column=4, padx=(5, 10))

import_btn = tk.Button(window, text="IMPORT", width=20, height=2, command=extract_images)
import_btn.pack(pady=10)

status_label = tk.Label(window, text="", bg="#5a7ca7", fg="white", font=("Segoe UI", 10))
status_label.pack(pady=5)

window.mainloop()
