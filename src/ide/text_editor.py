from PyQt5.QtWidgets import QTextEdit, QPushButton, QMessageBox, QFileDialog, QTabBar, QTabWidget
from PyQt5.QtGui import QColor, QTextCharFormat, QSyntaxHighlighter, QKeyEvent, QTextCursor
from PyQt5.QtCore import Qt, QSize, QRegularExpression

from pathlib import Path

from ide.settings import get_icon, settings
from ide.helpers import open_existing_file


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


class BaseEditor(QTextEdit):
    def __init__(self, filepath=None):
        super().__init__()
        # filepath exists at this point
        self.filepath = filepath
        self.saved = False
        if filepath is not None:
            # load the text and display it
            text = load_file(filepath)
            self.setText(text)
            self.saved = True
        self.setCurrentFont(settings.editor_font)
        self.textChanged.connect(self.changed)

    def keyPressEvent(self, event: QKeyEvent) -> None:
        if event.key() == Qt.Key_Delete:
            cursor = self.textCursor()
            if cursor.hasSelection():
                cursor.removeSelectedText()
        elif event.modifiers() & Qt.ControlModifier:
            if event.key() == Qt.Key_C:
                self.copy()
            elif event.key() == Qt.Key_V:
                self.paste()
            elif event.key() == Qt.Key_X:
                self.cut()
        else:
            QTextEdit.keyPressEvent(self, event)

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


class PythonEditor(BaseEditor):
    """
    A text editor which also handles the widget displayed in the tab, as well as displaying Python text
    """
    def __init__(self, filepath=None):
        super().__init__()
        self.highlighter = PythonSyntax(self.document())

    def keyPressEvent(self, event: QKeyEvent) -> None:
        if event.key() == Qt.Key_Tab:
            cursor = self.textCursor()
            current_pos = cursor.positionInBlock()
            spaces_to_add = 4 - (current_pos % 4)
            self.insertPlainText(' ' * spaces_to_add)
        elif event.key() == Qt.Key_Left or event.key() == Qt.Key_Right:
            self.move_cursor_to_tab(event)
        else:
            BaseEditor.keyPressEvent(self, event)

    def move_cursor_to_tab(self, event):
        cursor = self.textCursor()
        current_pos = cursor.positionInBlock()
        line_text = cursor.block().text()

        shift_pressed = event.modifiers() & Qt.ShiftModifier

        if event.key() == Qt.Key_Left:
            new_pos = (current_pos - 1) // 4 * 4
            if current_pos > 0 and line_text[current_pos:new_pos:-1].strip() == '':
                move_type = QTextCursor.KeepAnchor if shift_pressed else QTextCursor.MoveAnchor
                cursor.movePosition(QTextCursor.Left, move_type, n=(current_pos - new_pos))
            else:
                move_type = QTextCursor.KeepAnchor if shift_pressed else QTextCursor.MoveAnchor
                cursor.movePosition(QTextCursor.Left, move_type)

        elif event.key() == Qt.Key_Right:
            new_pos = ((current_pos + 4) // 4) * 4
            if new_pos < len(line_text) and line_text[current_pos:new_pos].strip() == '':
                move_type = QTextCursor.KeepAnchor if shift_pressed else QTextCursor.MoveAnchor
                cursor.movePosition(QTextCursor.Right, move_type, n=(new_pos - current_pos))
            else:
                move_type = QTextCursor.KeepAnchor if shift_pressed else QTextCursor.MoveAnchor
                cursor.movePosition(QTextCursor.Right, move_type)

        self.setTextCursor(cursor)


class TextEditorContainer(QTabWidget):
    def __init__(self):
        super().__init__()
        # start with an empty editor
        self.add_new_editor(PythonEditor())

    def add_new_editor(self, editor):
        index = self.addTab(editor, editor.tab_name)
        # we need to add something to the close button
        close_button = editor.get_tab_widget()
        close_button.clicked.connect(lambda: self.close_editor(editor))
        self.tabBar().setTabButton(index, QTabBar.ButtonPosition.RightSide, close_button)
        # move to this index
        self.setCurrentIndex(index)

    def close_editor(self, editor):
        # remove the tab, but let it handle itself first
        index = self.indexOf(editor)
        if index >= 0:
            # editor was found
            editor.close()
            self.removeTab(index)

    # define the base text actions
    def cut_text(self):
        current_tab = self.currentWidget()
        current_tab.cut()

    def paste_text(self, text):
        current_tab = self.currentWidget()
        current_tab.paste(text)

    def copy_text(self):
        current_tab = self.currentWidget()
        current_tab.copy()

    def delete_text(self):
        current_tab = self.currentWidget()
        cursor = current_tab.textCursor()
        if cursor.hasSelection():
            cursor.removeSelectedText()

    def new_file(self):
        self.add_new_editor(PythonEditor())

    def open_file(self):
        filepath = open_existing_file(self)
        if len(filepath) == 0:
            return
        filepath = Path(filepath)
        if filepath.suffix.lower() == '.py':
            self.add_new_editor(PythonEditor(filepath))
        else:
            self.add_new_editor(BaseEditor(filepath))
