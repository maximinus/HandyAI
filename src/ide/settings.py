import os
import yaml
from pathlib import Path

from PyQt5.QtWidgets import QDialog, QPushButton, QCheckBox, QComboBox, QVBoxLayout
from PyQt5.QtGui import QPixmap, QIcon, QFont
from PyQt5.QtCore import Qt

SETTINGS_FOLDER = Path.home() / '.handy'
CONFIG_SETTINGS = SETTINGS_FOLDER / 'config.yaml'


def get_yaml_data(yaml_file):
    with open(yaml_file, 'r') as file:
        yaml_data = yaml.safe_load(file)
    return yaml_data


class Settings:
    def __init__(self):
        self.config = get_yaml_data(CONFIG_SETTINGS)
        self.install_dir = Path(self.config['install']['directory'])
        if not os.path.exists(self.install_dir):
            raise EnvironmentError(f'Install directory {self.install_dir} not found')
        self.editor_font = QFont(self.config['font']['name'], self.config['font']['size'])


settings = Settings()


def get_icon(icon_name):
    return QIcon(str(settings.install_dir / 'media' / 'icons' / f'{icon_name}.svg'))


def get_pixmap(pixmap_name):
    return QPixmap(str(settings.install_dir / 'media' / 'icons' / f'{pixmap_name}.png'))


class SettingsWindow(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent, Qt.WindowTitleHint | Qt.WindowSystemMenuHint)

        layout = QVBoxLayout()
        self.textFontBtn = QPushButton('Select Text Font', self)
        #self.textFontBtn.clicked.connect(self.selectTextFont)
        layout.addWidget(self.textFontBtn)

        self.editorFontBtn = QPushButton('Select Editor Font', self)
        #self.editorFontBtn.clicked.connect(self.selectEditorFont)
        layout.addWidget(self.editorFontBtn)

        self.askOnExitCheckbox = QCheckBox('Ask on exit', self)
        layout.addWidget(self.askOnExitCheckbox)

        self.aiComboBox = QComboBox(self)
        self.aiComboBox.addItems(["AI-1", "AI-2", "AI-3"])
        layout.addWidget(self.aiComboBox)

        self.installDirBtn = QPushButton('Select Install Directory', self)
        #self.installDirBtn.clicked.connect(self.selectInstallDirectory)
        layout.addWidget(self.installDirBtn)

        self.setLayout(layout)
        self.setWindowTitle('Options')
        self.setGeometry(300, 300, 300, 200)


def show_settings(root_window):
    dialog = SettingsWindow(root_window)
    dialog.setModal(True)
    dialog.exec_()
