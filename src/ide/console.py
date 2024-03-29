from PyQt5.QtWidgets import QTextEdit
from PyQt5.QtGui import QTextCursor, QKeyEvent
from PyQt5.QtCore import Qt


class Console(QTextEdit):
    def __init__(self):
        super().__init__()
        self.setAcceptRichText(False)

    def keyPressEvent(self, event: QKeyEvent) -> None:
        if event.key() in (Qt.Key_Up, Qt.Key_Down):
            return
        super().keyPressEvent(event)

        # keep the cursor on the last line
        cursor = self.textCursor()
        cursor.movePosition(QTextCursor.End)
        self.setTextCursor(cursor)
