# -*- coding: utf-8 -*-
import os
import sys
import json
import gettext
import webbrowser
from PyQt5.QtWidgets import (
    QLabel, QApplication, QWidget, QVBoxLayout, QPushButton, QFileDialog,
    QListWidget, QMessageBox, QProgressBar, QHBoxLayout, QDialog
)
from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtGui import QPixmap, QIcon
from extractor import extract_images

SETTINGS_PATH = "settings.json"
RECENT_PATH = "recent.json"

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
    "ka": "Georgian",
    "es": "Español",
    "cs": "Čeština",
    "he": "עברית",
    "ar": "العربية",
    "pt": "Português"
}

def load_settings():
    if os.path.exists(SETTINGS_PATH):
        try:
            with open(SETTINGS_PATH, "r", encoding="utf-8") as f:
                return json.load(f)
        except:
            return {}
    return {}

def save_settings(data):
    with open(SETTINGS_PATH, "w", encoding="utf-8") as f:
        json.dump(data, f)

def resource_path(relative_path):
    if hasattr(sys, "_MEIPASS"):
        return os.path.join(sys._MEIPASS, relative_path)
    return os.path.join(os.path.abspath("."), relative_path)

class ClickableLabel(QLabel):
    clicked = pyqtSignal()
    def mouseReleaseEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.clicked.emit()
        super().mouseReleaseEvent(event)

class HarExtractorApp(QWidget):

    def __init__(self):
        super().__init__()
        self.settings = load_settings()
        self.setAcceptDrops(True)
        self.setWindowTitle("HAR Importer")

        self.lang_code = self.settings.get("lang")
        if not self.lang_code:
            self.lang_code = self.ask_language()
            self.settings["lang"] = self.lang_code
            save_settings(self.settings)

        self.apply_translation(self.lang_code)
        self.init_ui()
        self.retranslate_ui()

    def dragEnterEvent(self, event):
        if event.mimeData().hasUrls():
            for url in event.mimeData().urls():
                if url.toLocalFile().lower().endswith(".har"):
                    event.acceptProposedAction()
                    return
        event.ignore()

    def dropEvent(self, event):
        if event.mimeData().hasUrls():
            for url in event.mimeData().urls():
                path = url.toLocalFile()
                if path.lower().endswith(".har"):
                    self.loaded_file = path
                    self.info_label.setText(_("Загружен: ") + os.path.basename(path))
                    self.import_button.setEnabled(True)
                    self.cancel_button.setEnabled(True)
                    return
        QMessageBox.warning(self, _("Ошибка"), _("Файл должен быть в формате .har"))

    def ask_language(self):
        dlg = QDialog(self)
        dlg.setWindowTitle("Select Language")
        dlg.setMinimumSize(300, 500)
        layout = QVBoxLayout()
        label = QLabel("Choose your language / Выберите язык")
        label.setAlignment(Qt.AlignCenter)
        layout.addWidget(label)

        selected = {"code": None}
        for code, name in AVAILABLE_LANGUAGES.items():
            if not code.strip() or not name.strip():
                continue
            btn = QPushButton(name)
            btn.clicked.connect(lambda _, c=code: self._select_lang_and_close(dlg, selected, c))
            layout.addWidget(btn)

        dlg.setLayout(layout)
        dlg.exec_()
        return selected["code"] or "en"

    def _select_lang_and_close(self, dialog, selected, code):
        selected["code"] = code
        dialog.accept()

    def apply_translation(self, lang_code):
        global _
        locale_path = os.path.join(os.path.dirname(__file__), "locale")
        lang = gettext.translation("messages", localedir=locale_path, languages=[lang_code], fallback=True)
        lang.install()
        _ = lang.gettext

    def set_language(self, lang_code):
        self.lang_code = lang_code
        self.settings["lang"] = lang_code
        save_settings(self.settings)
        self.apply_translation(lang_code)

    def change_lang(self, code):
        self.set_language(code)
        self.retranslate_ui()
        QMessageBox.information(self, _("Язык изменён"), _("Интерфейс обновлён."))

    def init_ui(self):
        self.layout = QVBoxLayout()

        self.top_bar = QHBoxLayout()
        self.settings_button = QPushButton()
        self.settings_button.setIcon(QIcon(resource_path("assets/settings.png")))
        self.settings_button.setFixedSize(24, 24)
        self.settings_button.setIconSize(self.settings_button.size())
        self.settings_button.setStyleSheet("border: none;")
        self.settings_button.clicked.connect(self.open_settings)
        self.top_bar.addWidget(self.settings_button, alignment=Qt.AlignLeft)
        self.layout.addLayout(self.top_bar)

        self.main_screen = QWidget()
        self.main_layout = QVBoxLayout()
        self.main_screen.setLayout(self.main_layout)

        self.drop_image = ClickableLabel()
        self.drop_image.clicked.connect(self.load_file)
        self.drop_image.setAlignment(Qt.AlignCenter)
        pixmap = QPixmap(resource_path("assets/har_plus.png"))
        if not pixmap.isNull():
            self.drop_image.setPixmap(pixmap.scaledToWidth(128, Qt.SmoothTransformation))
        else:
            self.drop_image.setText("har_plus.png not found")
        self.main_layout.addWidget(self.drop_image)

        self.drop_text = QLabel(_("Перетащите .har файл сюда или нажмите ниже"))
        self.drop_text.setAlignment(Qt.AlignCenter)
        self.main_layout.addWidget(self.drop_text)

        self.info_label = QLabel()
        self.info_label.setAlignment(Qt.AlignCenter)
        self.main_layout.addWidget(self.info_label)

        self.progress_bar = QProgressBar()
        self.progress_bar.hide()
        self.main_layout.addWidget(self.progress_bar)

        self.load_button = QPushButton(_("Загрузить .har"))
        self.load_button.clicked.connect(self.load_file)
        self.main_layout.addWidget(self.load_button)

        self.import_button = QPushButton(_("Импорт"))
        self.import_button.setEnabled(False)
        self.import_button.clicked.connect(self.import_data)
        self.main_layout.addWidget(self.import_button)

        self.cancel_button = QPushButton(_("Отмена"))
        self.cancel_button.setEnabled(False)
        self.cancel_button.clicked.connect(self.reset)
        self.main_layout.addWidget(self.cancel_button)

        self.recent_label = QLabel(_("Недавние папки импорта:"))
        self.main_layout.addWidget(self.recent_label)

        self.recent_list = QListWidget()
        self.recent_list.itemDoubleClicked.connect(self.open_recent_folder)
        self.main_layout.addWidget(self.recent_list)

        self.settings_screen = QWidget()
        self.settings_layout = QVBoxLayout()
        self.settings_screen.setLayout(self.settings_layout)
        self.settings_screen.hide()

        self.language_label = QLabel(_("Выберите язык:"))
        self.language_label.setAlignment(Qt.AlignCenter)
        self.settings_layout.addWidget(self.language_label)

        self.language_buttons = []
        for code, name in AVAILABLE_LANGUAGES.items():
            if not code.strip() or not name.strip():
                continue
            btn = QPushButton(_(name))
            btn.clicked.connect(lambda _, c=code: self.change_lang(c))
            self.settings_layout.addWidget(btn)
            self.language_buttons.append(btn)

        self.clear_history_button = QPushButton(_("Очистить историю"))
        self.back_button = QPushButton(_("← Назад"))
        self.settings_layout.addWidget(self.clear_history_button)
        self.settings_layout.addWidget(self.back_button)
        self.clear_history_button.clicked.connect(self.clear_history)
        self.back_button.clicked.connect(self.close_settings)

        self.layout.addWidget(self.main_screen)
        self.layout.addWidget(self.settings_screen)
        self.setLayout(self.layout)
        self.refresh_recent()

    def retranslate_ui(self):
        self.setWindowTitle(_("HAR Importer"))
        self.drop_text.setText(_("Перетащите .har файл сюда или нажмите ниже"))
        self.load_button.setText(_("Загрузить .har"))
        self.import_button.setText(_("Импорт"))
        self.cancel_button.setText(_("Отмена"))
        self.recent_label.setText(_("Недавние папки импорта:"))
        self.language_label.setText(_("Выберите язык:"))
        for i, code in enumerate(AVAILABLE_LANGUAGES):
            if i < len(self.language_buttons):
                self.language_buttons[i].setText(_(AVAILABLE_LANGUAGES[code]))
        self.clear_history_button.setText(_("Очистить историю"))
        self.back_button.setText(_("← Назад"))

    def open_settings(self):
        self.main_screen.hide()
        self.settings_screen.show()

    def close_settings(self):
        self.settings_screen.hide()
        self.main_screen.show()

    def refresh_recent(self):
        self.recent_list.clear()
        if os.path.exists(RECENT_PATH):
            try:
                with open(RECENT_PATH, "r", encoding="utf-8") as f:
                    paths = json.load(f)
                    for p in paths:
                        self.recent_list.addItem(p)
            except Exception as e:
                print(f"Error loading recent paths: {e}")

    def update_recent(self, folder):
        paths = []
        if os.path.exists(RECENT_PATH):
            try:
                with open(RECENT_PATH, "r", encoding="utf-8") as f:
                    paths = json.load(f)
            except:
                paths = []
        if folder in paths:
            paths.remove(folder)
        paths.insert(0, folder)
        paths = paths[:10]
        with open(RECENT_PATH, "w", encoding="utf-8") as f:
            json.dump(paths, f)
        self.refresh_recent()

    def open_recent_folder(self, item):
        path = item.text()
        if os.path.exists(path):
            webbrowser.open(path)
        else:
            QMessageBox.warning(self, _("Ошибка"), f"{path}\n{_('Папка недоступна или удалена.')}")

    def load_file(self):
        file_name, __ = QFileDialog.getOpenFileName(self, _("Выбрать .har файл"), "", "HAR Files (*.har)")
        if file_name:
            self.loaded_file = file_name
            self.info_label.setText(_("Загружен: ") + os.path.basename(self.loaded_file))
            self.import_button.setEnabled(True)
            self.cancel_button.setEnabled(True)

    def reset(self):
        self.loaded_file = None
        self.info_label.setText("")
        self.import_button.setEnabled(False)
        self.cancel_button.setEnabled(False)
        self.progress_bar.hide()

    def import_data(self):
        if not self.loaded_file:
            return
        target_dir = QFileDialog.getExistingDirectory(self, _("Выбрать папку для сохранения"))
        if not target_dir:
            return
        self.progress_bar.show()
        self.progress_bar.setValue(0)

        def update_progress(val):
            self.progress_bar.setValue(val)

        try:
            extracted = extract_images(self.loaded_file, target_dir, progress_callback=update_progress)
        except Exception as e:
            QMessageBox.warning(self, _("Ошибка"), f"{_('Не удалось прочитать файл:')}\n{e}")
            self.progress_bar.hide()
            return

        self.progress_bar.hide()
        QMessageBox.information(self, _("Готово"), f"{_('Извлечено изображений:')} {extracted}")
        self.update_recent(target_dir)

    def clear_history(self):
        if os.path.exists(RECENT_PATH):
            os.remove(RECENT_PATH)
        self.refresh_recent()
        QMessageBox.information(self, _("Готово"), _("История очищена."))

def run_app():
    app = QApplication(sys.argv)
    from PyQt5.QtGui import QFont
    font = QFont("Segoe UI", 10)
    app.setFont(font)
    window = HarExtractorApp()
    window.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    run_app()
