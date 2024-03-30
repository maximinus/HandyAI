from PyQt5.QtWidgets import QFileDialog


def open_existing_file(widget):
    # Get file from user - returns '' with no file
    filename, _ = QFileDialog.getOpenFileName(widget, 'Open file', '', 'All files (*.*)')
    return filename
