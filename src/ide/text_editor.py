from PyQt5.QtWidgets import QTextEdit, QWidget, QHBoxLayout, QLabel, QPushButton
from PyQt5.QtCore import QSize

from ide.settings import get_icon, get_pixmap


def get_close_button():
    close_button = QPushButton()
    close_button.setIcon(get_icon('close-button'))
    close_button.setIconSize(QSize(12, 12))
    close_button.setStyleSheet('border: none;')
    return close_button


class PythonEditor(QTextEdit):
    """
    A text editor which also handles the widget displayed in the tab, as well as displaying Python text
    """
    def __init__(self, filepath=None):
        super().__init__()
        self.filepath = filepath
        # must be saved when we first open the file
        self.saved = True

    @property
    def tab_name(self):
        if self.filepath is None:
            return 'new file'
        else:
            return self.filepath.name

    def get_tab_widget(self):
        return get_close_button()
