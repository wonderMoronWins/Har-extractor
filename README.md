# IHAR — HAR Image Extractor
![HAR Banner](./assets/har-banner.png)

> A small tool to extract embedded images from `.har` files exported via browser DevTools.  
> Simple. Open-source. Developed with modern LLM-based tools.

## 📌 What it does

IHAR extracts images directly embedded (as base64) inside `.har` files — useful for preserving media when access to source links is lost or blocked.

You can:
- Select a `.har` file exported from Chrome/Firefox/Edge
- Extract all images (PNG, JPEG, WEBP, AVIF...)
- Save them into a folder of your choice

## ⚙ How to use

### ✅ Recommended: Windows `.exe` version
1. Download and run `extractor_gui.exe`
2. Open your browser (Chrome / Edge / Firefox), press `F12`, go to `Network` tab
3. Reload the target page and filter by `img`
4. Right-click → `Save all as HAR with content`
5. Select the saved `.har` file in the app
6. Click `IMPORT` — extracted images will appear in the output folder

Works without Python. No installation needed.

### 🐍 Alternative: Run from source
- `pip install haralyzer pillow`
- `python extractor_gui.py`

## 🤖 Why this was created

> "This is not an attempt to pose as a developer, but a way to share a simple, working tool."

The author is passionate about IT, neural networks, and programming in general.  
This project was developed independently using modern coding practices.  
Some code blocks were refined using LLM-based assistants as part of the workflow.

## 📖 License & Attribution

> 📝 This project is licensed under the **GNU GPLv3**.  
> You are free to use, modify, and redistribute this software, but you **must**:
> 
> - 🔒 Keep the original license (GPLv3)
> - 🙋 Mention the original author (2025)
> - 📂 Provide source code if you distribute a modified version

---
> 💡 This tool was created independently, with the help of automated assistants (LLM tools) for template generation and refactoring.  
> All design decisions and logic were authored manually.
>  
> 🧑 Author: Егорин Евгений Александрович  
> 🌍 Автор (EN): Egorin Eugene Alexandrovich  
> 🔗 GitHub: [wonderMoronWins](https://github.com/wonderMoronWins)  
> 📅 Год: 2025

---

## 📘 Overview: LLM-assisted workflow, not AI authorship
The project was built using LLM-based tools for code generation and review, while all logic and decisions were made by the author.

# IHAR — Извлечение изображений из HAR

> Простая утилита для извлечения изображений из файлов `.har`, экспортированных из браузеров.

## 📌 What the program does / Что делает программа

**EN:**

IHAR extracts images encoded in base64 and embedded in `.har` files. This is useful when:
- The original page is no longer accessible
- The source requires login/authentication
- You want to grab images from dynamic content

**RU:**

IHAR извлекает изображения, закодированные в base64 и встроенные в `.har`-файлы. Это полезно, если:
- Страница больше недоступна
- Источник защищён / требует авторизации
- Нужно достать картинки с сайта, где всё динамически

## ⚙ How to use / Как пользоваться

**EN:**

### 🟢 If you use the `.exe` version:
1. Run `extractor_gui.exe`
2. In browser, press `Ctrl+Shift+I` (or `F12`) → go to `Network` tab
3. Reload the page, filter by `img`
4. Right-click → `Save all as HAR with content`
5. Select the `.har` file in the program
6. Click `IMPORT` — images will be extracted to selected folder

### 🐍 If you run from source:
- `pip install haralyzer pillow`
- `python extractor_gui.py`

**RU:**

### 🟢 Если у вас `.exe`:
1. Запустите `extractor_gui.exe`
2. В браузере нажмите `Ctrl+Shift+I` (или `F12`), вкладка `Сеть (Network)`
3. Обновите страницу, установите фильтр `img`
4. ПКМ → `Сохранить как HAR с содержимым (Save all as HAR with content)`
5. Выберите сохранённый `.har` в программе
6. Нажмите `IMPORT` — изображения появятся в выбранной папке

### 🐍 Если запускаете из кода:
- `pip install haralyzer pillow`
- `python extractor_gui.py`

## 💡 Почему это сделано

Автор не пытается выдать себя за программиста. Он хочет сделать доступным понятный, работающий инструмент.  
Проект создан с использованием современных LLM-инструментов, и это открыто указывается.  
Интерес — в IT, нейросетях, автоматизации и простых решениях для повседневных задач.

## 📖 Лицензия и открытость

Проект распространяется по лицензии **GNU GPLv3**. Это означает:

- Исходный код открыт — вы можете изменять, распространять и собирать под себя
- **Обязательное условие**: сохранять указание автора и лицензии GPLv3
- При переработке проекта необходимо предоставить исходный код
- Программа разработана автором самостоятельно, с применением LLM-ассистентов (например, ChatGPT) для генерации шаблонов. Все архитектурные решения — авторские.

---

## ℹ️ Author

This project was created by Egorin Eugene Alexandrovich (2025)  
Developed using LLM-assisted workflow (code templates and reviews only).
