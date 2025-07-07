
# -*- coding: utf-8 -*-
# Импорт модулей / Import modules
import tkinter as tk
from tkinter import filedialog, messagebox
from extractor import extract_images
import gettext
import os

# Глобальные переменные и путь к переводам / Globals and locale path
selected_har = ""
selected_folder = ""
current_lang = 'en'
localedir = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'locale')

# Загрузка перевода / Load translation
def load_translation(lang_code):
    global _
    lang = gettext.translation('messages', localedir=localedir, languages=[lang_code], fallback=True)
    lang.install()
    _ = lang.gettext

# Установка языка / Set language
def set_language(lang_code):
    global current_lang
    current_lang = lang_code
    load_translation(lang_code)
    update_texts()

# Обновление всех надписей в интерфейсе / Refresh GUI texts
def update_texts():
    root.title(_("Import .har"))
    title_label.config(text=_("Import .har"))
    har_btn.config(text=_("Select .har file"))
    folder_btn.config(text=_("Select output folder"))
    import_btn.config(text=_("IMPORT"))
    format_label.config(text=_(".jpg"))

# Выбор HAR-файла / Select HAR file
def select_har():
    global selected_har
    path = filedialog.askopenfilename(
        title=_("Select .har file"),
        filetypes=[("HAR files", "*.har")]
    )
    if path:
        selected_har = path
        har_label.config(text=path.split("/")[-1])

# Выбор папки сохранения / Select output folder
def select_folder():
    global selected_folder
    path = filedialog.askdirectory(title=_("Select output folder"))
    if path:
        selected_folder = path
        folder_label.config(text=path.split("/")[-1])

# Запуск импорта / Run import
def run_import():
    if not selected_har or not selected_folder:
        messagebox.showwarning("Missing", _("Select both .har file and output folder"))
        return
    count = extract_images(selected_har, selected_folder)
    messagebox.showinfo("Done", _("Extracted {count} images to /img").format(count=count))

# Начальная загрузка языка / Load default language
load_translation(current_lang)

# Настройка окна / GUI setup
root = tk.Tk()
root.title(_("Import .har"))
root.geometry("500x300")
root.configure(bg='#6b90aa')

# Меню: Settings → Language / Top menu
menubar = tk.Menu(root)
settings_menu = tk.Menu(menubar, tearoff=0)
lang_menu = tk.Menu(settings_menu, tearoff=0)

lang_menu.add_command(label="English", command=lambda: set_language("en"))
lang_menu.add_command(label="Русский", command=lambda: set_language("ru"))
lang_menu.add_command(label="Українська", command=lambda: set_language("uk"))

settings_menu.add_cascade(label="Language", menu=lang_menu)
menubar.add_cascade(label="Settings", menu=settings_menu)
root.config(menu=menubar)

# Заголовок / Title label
title_label = tk.Label(root, text=_("Import .har"), font=("Arial", 18, "bold"), bg='#6b90aa', fg='white')
title_label.pack(pady=15)

# Основной блок выбора / File and folder selection area
frame = tk.Frame(root, bg='#6b90aa')
frame.pack()

har_btn = tk.Button(frame, text=_("Select .har file"), command=select_har)
har_btn.grid(row=0, column=0, padx=10)

arrow_label = tk.Label(frame, text="→", font=("Arial", 14), bg='#6b90aa', fg='white')
arrow_label.grid(row=0, column=1)

format_label = tk.Label(frame, text=_(".jpg"), font=("Arial", 12, "bold"), bg='white', relief='sunken', width=6)
format_label.grid(row=0, column=2, padx=10)

arrow2_label = tk.Label(frame, text="→", font=("Arial", 14), bg='#6b90aa', fg='white')
arrow2_label.grid(row=0, column=3)

folder_btn = tk.Button(frame, text=_("Select output folder"), command=select_folder)
folder_btn.grid(row=0, column=4, padx=10)

# Метки с выбранными путями / Display selected paths
har_label = tk.Label(root, text="", bg='#6b90aa', fg='white', font=("Arial", 10))
har_label.pack()

folder_label = tk.Label(root, text="", bg='#6b90aa', fg='white', font=("Arial", 10))
folder_label.pack()

# Кнопка импорта / Import button
import_btn = tk.Button(root, text=_("IMPORT"), font=("Arial", 12, "bold"), bg='white', command=run_import)
import_btn.pack(pady=25)

# Запуск интерфейса / Start GUI loop
root.mainloop()
