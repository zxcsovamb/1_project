import sys
import wget
import os
import random
import hashlib
import tempfile
import subprocess
import platform
from random import choice
from PyQt6.QtWidgets import (
    QApplication, QWidget, QPushButton, QLabel, QVBoxLayout, QHBoxLayout,
    QMessageBox, QDialog, QGridLayout, QLineEdit, QStackedLayout, QFileDialog
)
from PyQt6.QtGui import QPalette, QColor
from PyQt6.QtCore import Qt
import zipfile

def open_file(path):
    if platform.system() == "Windows":
        os.startfile(path)
    elif platform.system() == "Darwin":  # macOS
        subprocess.run(["open", path])
    else:  # Linux
        subprocess.run(["xdg-open", path])


color_list = ['Indigo', 'SlateBlue', 'DarkSlateBlue', 'DarkMagenta', 'Cornsilk',
              'RosyBrown', 'Chocolate', 'Gray', 'Maroon', 'Teal', 'MediumSlateBlue', 'PowderBlue',
              'ForestGreen', 'LawnGreen', 'Linen', 'DarkSlateGray', 'LightYellow', 'LightSalmon',
              'GreenYellow', 'SeaGreen', 'Khaki', 'Fuchsia', 'PeachPuff', 'OliveDrab']


class HashSelectionDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        layout = QGridLayout()
        algorithms = ["MD5", "SHA256", "SHA512", "SHA1"]
        for i, algo in enumerate(algorithms):
            btn = QPushButton(algo)
            btn.clicked.connect(lambda _, a=algo.lower(): self.select_algorithm(a))
            layout.addWidget(btn, i // 2, i % 2)
        self.setLayout(layout)

    def select_algorithm(self, algorithm):
        self.algorithm_selected = algorithm
        self.accept()


class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setFixedSize(850, 500)
        palette = QPalette()
        palette.setColor(QPalette.ColorRole.Window, QColor('NavajoWhite'))
        self.setPalette(palette)
        self.setAutoFillBackground(True)

        main_layout = QVBoxLayout(self)

        # Кнопки сверху
        button_layout = QHBoxLayout()
        self.buttons = []
        for name, method in [("Изменение цвета", self.show_home),
                             ("Установщики", self.show_installers),
                             ("Хеширование", self.show_hashing),
                             ("Рандомайзер", self.show_randomizer)]:
            btn = QPushButton(name)
            btn.setStyleSheet(self.button_style())
            btn.clicked.connect(method)
            self.buttons.append(btn)
            button_layout.addWidget(btn)

        main_layout.addLayout(button_layout)

        # Стек страниц
        self.stack = QStackedLayout()
        main_layout.addLayout(self.stack)

        # Главная страница
        self.page_home = QLabel("Привет, " + os.getlogin())
        self.page_home.setStyleSheet('font-size: 20px')
        self.page_home.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.stack.addWidget(self.page_home)

        # Плейсхолдеры для других страниц
        self.page_installers = QWidget()
        self.page_hashing = QWidget()
        self.page_randomizer = QWidget()

        self.show_home()

    def button_style(self):
        return ('background-color: BurlyWood; font-size: 16px; padding: 10px; border-radius: 5px;')

    def show_home(self):
        bg_color = choice(color_list)
        palette = self.palette()
        palette.setColor(QPalette.ColorRole.Window, QColor(bg_color))
        self.setPalette(palette)

    def show_installers(self):
        layout = QVBoxLayout()
        items = [("Anydesk", self.download_anydesk),("AnVir",self.download_anvir), ("Chrome", self.download_chrome),(".NET Framework", self.download_net),("Visual C++", self.download_Visual_C),("AHK", self.download_ahk),("zapret", self.zapret)]
        for name, func in items:
            hlayout = QHBoxLayout()
            label = QLabel(name)
            label.setStyleSheet('font-size: 20px')
            btn = QPushButton('Скачать')
            btn.setStyleSheet(self.button_style())
            btn.clicked.connect(func)
            hlayout.addWidget(label)
            hlayout.addWidget(btn)
            layout.addLayout(hlayout)

        self.page_installers.setLayout(layout)
        if self.stack.indexOf(self.page_installers) == -1:
            self.stack.addWidget(self.page_installers)
        self.stack.setCurrentWidget(self.page_installers)

    def download_anydesk(self):
        url = "https://github.com/zxcsovamb/1_project/raw/refs/heads/main/anydesk.exe"
        self.download_and_chose(url,"Anydesk")
    def download_anvir(self):
        url = "https://github.com/zxcsovamb/1_project/raw/refs/heads/main/AnVir.exe"
        self.download_and_chose(url,"AnVir")
    def download_chrome(self):
        url = "https://github.com/zxcsovamb/1_project/raw/refs/heads/main/ChromeSetup.exe"
        self.download_and_chose(url,"Chrome")

    def download_net(self):
        url = "https://github.com/zxcsovamb/1_project/raw/refs/heads/main/ndp481-x86-x64-allos-rus.exe"
        self.download_and_chose(url,"ndp481-x86-x64-allos-rus.exe")

    def download_Visual_C(self):
        url = "https://github.com/zxcsovamb/1_project/raw/refs/heads/main/VC_redist.exe"
        self.download_and_chose(url,"vc_redist.exe")

    def download_ahk(self):
        url = "https://github.com/zxcsovamb/1_project/raw/refs/heads/main/AHK.exe"
        self.download_and_chose(url, "AHK.exe")

    def zapret(self):
        url = "https://github.com/zxcsovamb/1_project/raw/refs/heads/main/zapret.zip"
        self.download_and_chose(url, "zapret.zip")

    def download_and_chose(self, url, name):
        try:
            QMessageBox.information(self, "None", "Выберете куда скачать файл")
            dir_path = self.choose_directory()
            wget.download(url, out=dir_path)
            QMessageBox.information(self, "Успех", f"{name} успешно загружен")
        except Exception as e:
            QMessageBox.critical(self, "Ошибка", str(e))
    def download(self, url, dir_path, name):
        try:
            wget.download(url, out=dir_path)
            QMessageBox.information(self, "Успех", f"{name} успешно загружен")
        except Exception as e:
            QMessageBox.critical(self, "Ошибка", str(e))
    def choose_directory(self):
        dialog = QFileDialog()
        dialog.setFileMode(QFileDialog.FileMode.Directory)
        if dialog.exec():
            return dialog.selectedFiles()[0]
        return None

    def show_hashing(self):
        layout = QVBoxLayout()
        input_field = QLineEdit()
        input_field.setPlaceholderText("Введите строку для хэширования...")
        input_field.setStyleSheet('font-size: 16px; padding: 10px; border-radius: 5px; background-color: WhiteSmoke;')
        submit_button = QPushButton("Выбрать алгоритм")
        submit_button.setStyleSheet(self.button_style())
        submit_button.clicked.connect(lambda: self.open_hash_selection(input_field.text()))

        layout.addWidget(input_field)
        layout.addWidget(submit_button)
        self.page_hashing.setLayout(layout)
        if self.stack.indexOf(self.page_hashing) == -1:
            self.stack.addWidget(self.page_hashing)
        self.stack.setCurrentWidget(self.page_hashing)

    def open_hash_selection(self, data_to_hash):
        dialog = HashSelectionDialog(self)
        result = dialog.exec()
        if result == QDialog.DialogCode.Accepted and hasattr(dialog, 'algorithm_selected'):
            self.calculate_hash(data_to_hash, dialog.algorithm_selected)

    def calculate_hash(self, data, algorithm):
        try:
            hash_funcs = {
                "md5": hashlib.md5,
                "sha256": hashlib.sha256,
                "sha512": hashlib.sha512,
                "sha1": hashlib.sha1
            }
            hashed_data = hash_funcs[algorithm](data.encode()).hexdigest()
            QApplication.clipboard().setText(hashed_data)
            QMessageBox.information(self, "Результат хэширования",
                                    f"Алгоритм: {algorithm.upper()} \n\n"
                                    f"Хэш:\n{hashed_data} \n\n"
                                    f"Скопировано в буфер обмена!")
        except Exception as e:
            QMessageBox.critical(self, "Ошибка", str(e))

    def show_randomizer(self):
        number = str(random.randint(1, 9999999999))
        dlg = QMessageBox(self)
        dlg.setWindowTitle("Рандомайзер")
        dlg.setText(f"Число: {number} Скопировать?")
        dlg.setStandardButtons(QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
        dlg.setIcon(QMessageBox.Icon.Question)
        button = dlg.exec()

        if button == QMessageBox.StandardButton.Yes:
            QApplication.clipboard().setText(number)
            QMessageBox.information(self, "Окно", "Успешно!")


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())

