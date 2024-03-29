from PyQt5.QtWidgets import QFileDialog

# general code helpers


def get_exisiting_file(widget):
    # Get file from user
    filename, _ = QFileDialog.getOpenFileName(widget, 'Open file', '', 'All files (*.*)')
    return filename
