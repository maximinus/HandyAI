from PyQt5.QtWidgets import QTextEdit, QPushButton
from PyQt5.QtGui import QColor, QTextCharFormat, QFont, QSyntaxHighlighter
from PyQt5.QtCore import QSize, QRegularExpression

from ide.settings import get_icon, get_pixmap


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


class PythonEditor(QTextEdit):
    """
    A text editor which also handles the widget displayed in the tab, as well as displaying Python text
    """
    def __init__(self, filepath=None):
        super().__init__()
        self.filepath = filepath
        # must be saved when we first open the file
        self.saved = True
        self.highlighter = PythonSyntax(self.document())

    @property
    def tab_name(self):
        if self.filepath is None:
            return 'new file'
        else:
            return self.filepath.name

    def get_tab_widget(self):
        return get_close_button()
