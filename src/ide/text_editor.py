from PyQt5.QtWidgets import QTextEdit, QPushButton, QMessageBox, QFileDialog
from PyQt5.QtGui import QColor, QTextCharFormat, QSyntaxHighlighter
from PyQt5.QtCore import QSize, QRegularExpression

from ide.settings import get_icon


def get_close_button():
    close_button = QPushButton()
    close_button.setIcon(get_icon('close-button'))
    close_button.setIconSize(QSize(12, 12))
    close_button.setStyleSheet('border: none;')
    return close_button


class PythonSyntax(QSyntaxHighlighter):
    # Syntax highlighter for Python
    def __init__(self, document):
        super().__init__(document)

        # Define syntax highlighting rules
        keyword_format = QTextCharFormat()
        keyword_format.setForeground(QColor('blue'))
        keywords = [
            'and', 'as', 'assert', 'break', 'class', 'continue', 'def', 'del', 'elif', 'else',
            'except', 'finally', 'for', 'from', 'global', 'if', 'import', 'in', 'is', 'lambda',
            'nonlocal', 'not', 'or', 'pass', 'raise', 'return', 'try', 'while', 'with', 'yield'
        ]
        self.highlighting_rules = [(QRegularExpression(r'\b' + keyword + r'\b'), keyword_format)
                                   for keyword in keywords]

        # String literal
        string_format = QTextCharFormat()
        string_format.setForeground(QColor('magenta'))
        self.highlighting_rules.append((QRegularExpression(r'"[^"\\]*(\\.[^"\\]*)*"'), string_format))
        self.highlighting_rules.append((QRegularExpression(r"'[^'\\]*(\\.[^'\\]*)*'"), string_format))

        # Single-line comment
        single_line_comment_format = QTextCharFormat()
        single_line_comment_format.setForeground(QColor('green'))
        self.highlighting_rules.append((QRegularExpression(r'#.*'), single_line_comment_format))

    def highlightBlock(self, text):
        for pattern, format in self.highlighting_rules:
            match_iterator = pattern.globalMatch(text)
            while match_iterator.hasNext():
                match = match_iterator.next()
                self.setFormat(match.capturedStart(), match.capturedLength(), format)

        self.setCurrentBlockState(0)


def load_file(filepath):
    with open(filepath, 'r') as f:
        return f.read()


class PythonEditor(QTextEdit):
    """
    A text editor which also handles the widget displayed in the tab, as well as displaying Python text
    """
    def __init__(self, filepath=None):
        super().__init__()
        # filepath exists at this point
        self.filepath = filepath
        self.saved = False
        if filepath is not None:
            # load the text and display it
            text = load_file()
            self.setText(text)
            self.saved = True
        self.highlighter = PythonSyntax(self.document())
        self.textChanged.connect(self.changed)

    def changed(self):
        # text has been modified, so this version has not been changed
        self.saved = False

    @property
    def tab_name(self):
        if self.filepath is None:
            return 'new file'
        else:
            return self.filepath.name

    def get_tab_widget(self):
        return get_close_button()

    def close(self):
        # called just before the resource is destroyed
        # if we have been saved, no need to do anything
        if self.saved is True:
            return
        reply = QMessageBox.question(self, 'Save?', 'Save file before closing?',
                                     QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if reply == QMessageBox.Yes:
            self.save_file()

    def save_file(self):
        extension = 'All files (*.*)'
        if self.filepath is not None:
            extension = f'*{self.filepath.suffix}'

        # we need to save with some kind of name
        filename, _ = QFileDialog.getSaveFileName(self, 'Save File', '', 'All files (*.*)')
        if filename:
            with open(filename, 'w') as file:
                text = self.toPlainText()
                file.write(text)
        self.saved = True
