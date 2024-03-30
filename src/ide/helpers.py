from PyQt5.QtWidgets import QDialog, QVBoxLayout, QLabel, QPushButton, QFileDialog
from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt

from ide.settings import get_pixmap


def open_existing_file(widget):
    # Get file from user - returns '' with no file
    filename, _ = QFileDialog.getOpenFileName(widget, 'Open file', '', 'All files (*.*)')
    return filename


class AboutScreen(QDialog):
    def __init__(self):
        super().__init__()

        # Initialize layout
        layout = QVBoxLayout()
        layout.setContentsMargins(20, 20, 20, 20)

        # Create and add the image
        image_label = QLabel(self)
        image_label.setPixmap(get_pixmap('handy_logo'))
        image_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(image_label)

        title_label = QLabel('Handy AI', self)
        title_font = QFont()
        title_font.setPointSize(20)
        title_label.setFont(title_font)
        title_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(title_label)

        info_label = QLabel('Python IDE with AI assist.\nCopr. Chris Handy 2024', self)
        info_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(info_label)

        ok_button = QPushButton("OK", self)
        ok_button.clicked.connect(self.close)
        layout.addWidget(ok_button)

        self.setLayout(layout)
        self.setWindowTitle('Handy AI')


def show_about_screen():
    screen = AboutScreen()
    screen.exec_()
