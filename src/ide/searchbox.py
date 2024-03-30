from PyQt5.QtWidgets import QWidget, QLineEdit, QHBoxLayout, QSizePolicy, QLabel, QPushButton
from PyQt5.QtCore import QSize

from ide.settings import get_icon


def add_search(toolbar):
    spacer = QWidget()
    spacer.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)
    toolbar.addWidget(spacer)

    widget = QWidget()
    search_area = QHBoxLayout()
    search_area.setContentsMargins(0, 0, 0, 0)

    # label to show matches
    label = QLabel('')
    # back and forward buttons
    previous = QPushButton()
    previous.setIcon(get_icon('previous'))
    previous.setIconSize(QSize(12, 12))
    previous.setStyleSheet('border: none;')
    next = QPushButton()
    next.setIcon(get_icon('next'))
    next.setIconSize(QSize(12, 12))
    next.setStyleSheet('border: none;')
    # textbox to enter search
    searchbox = QLineEdit()

    search_area.addWidget(label)
    search_area.addWidget(previous)
    search_area.addWidget(next)
    search_area.addWidget(searchbox)
    widget.setLayout(search_area)

    toolbar.addWidget(widget)
