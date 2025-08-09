import os
import sys
import json
from PyQt5.QtWidgets import QApplication, QDialog, QVBoxLayout, QLabel, QPushButton
from PyQt5.QtCore import Qt

CONFIG_FILE = "settings.json"

AVAILABLE_LANGUAGES = {
    "ru": "Русский",
    "en": "English",
    "uk": "Українська",
    "ja": "日本語",
    "ko": "한국어",
    "kk": "Қазақша",
    "de": "Deutsch",
    "fr": "Français",
    "it": "Italiano",
    "zh": "中文",
    "hy": "Հայերեն",
    "ka": "ქართული",
    "es": "Español",
    "cs": "Čeština",
    "he": "עברית",
    "ar": "العربية",
    "pt": "Português"
}

class LanguagePrompt(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Select Language")
        self.setFixedSize(300, 500)
        layout = QVBoxLayout()
        label = QLabel("Choose your language / Выберите язык")
        label.setAlignment(Qt.AlignCenter)
        layout.addWidget(label)

        for code, name in AVAILABLE_LANGUAGES.items():
            btn = QPushButton(name)
            btn.clicked.connect(lambda _, c=code: self.select_language(c))
            layout.addWidget(btn)

        self.setLayout(layout)

    def select_language(self, lang_code):
        with open(CONFIG_FILE, "w", encoding="utf-8") as f:
            json.dump({"lang": lang_code}, f)
        self.accept()

def choose_language():
    app = QApplication(sys.argv)
    prompt = LanguagePrompt()
    if prompt.exec_() == QDialog.Accepted:
        sys.exit(0)
    else:
        sys.exit(1)

if __name__ == "__main__":
    choose_language()