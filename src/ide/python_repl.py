from contextlib import redirect_stdout
from io import StringIO

from PyQt5.QtWidgets import QTextEdit, QVBoxLayout, QLineEdit, QWidget
from PyQt5.QtCore import pyqtSignal, QObject
from PyQt5 import QtGui

from ide.settings import settings

OUTPUT_COLOR = QtGui.QColor(0, 0, 128)


class OutputEmitter(QObject):
    write_text = pyqtSignal(str)

    def __init__(self):
        super().__init__()
        self.output_capture = StringIO()

    def write(self, text):
        self.output_capture.write(text)
        self.write_text.emit(text)

    def get_value(self):
        return self.output_capture.getvalue()


class PythonREPL(QWidget):
    def __init__(self):
        super().__init__()
        self.environment = {}
        layout = QVBoxLayout(self)
        self.output = QTextEdit()
        self.output.setCurrentFont(settings.editor_font)
        self.output.setReadOnly(True)
        self.input = QLineEdit()
        self.input.setFont(settings.editor_font)
        self.input.returnPressed.connect(self.run_code)
        layout.addWidget(self.output)
        layout.addWidget(self.input)
        self.setLayout(layout)

    def update_output(self, text, user=False):
        cursor = self.output.textCursor()
        if user is False:
            text_format = QtGui.QTextCharFormat()
            text_format.setFontItalic(True)
            text_format.setForeground(QtGui.QBrush(OUTPUT_COLOR))
            cursor.setCharFormat(text_format)
        cursor.insertText(text)
        cursor.setCharFormat(QtGui.QTextCharFormat())
        self.output.setTextCursor(cursor)

    def run_code(self):
        code = self.input.text()
        self.update_output(f'{code}\n', user=True)
        self.input.clear()
        output_capture = OutputEmitter()
        output_capture.write_text.connect(self.update_output)
        try:
            with redirect_stdout(output_capture):
                try:
                    result = eval(code, self.environment)
                    if result is not None:
                        # don't forget this is captured, so we won't see it here
                        print(result)
                except SyntaxError:
                    exec(code, self.environment)
        except Exception as ex:
            self.update_output(f'{ex}')
