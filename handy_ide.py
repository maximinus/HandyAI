import sys

from PyQt5.QtWidgets import (QApplication, QMainWindow, QTextEdit, QTreeView,
                             QSplitter, QTabWidget, QTabBar, QFileDialog)
from PyQt5.QtCore import Qt

from ide.settings import settings, get_all_actions, get_menu_setup, get_toolbar_setup
from ide.text_editor import PythonEditor
from ide.file_tree import FileTreeView
from ide.console import Console
from ide.llm_chat import LlmChat
from ide.python_tree import PythonTree


DEFAULT_WINDOW_SIZE = [1024, 768]
# this is based on the height
MAIN_WIDGET_RATIO = [568, 200]
# and then the width
SUB_WIDGET_RATIO = [300, 724]


class TextEditor(QMainWindow):
    def __init__(self):
        super().__init__()
        self.create_menu_and_toolbar()

        main_widget = QSplitter(Qt.Vertical)
        self.setCentralWidget(main_widget)
        top_splitter = QSplitter(Qt.Horizontal)
        main_widget.addWidget(top_splitter)

        # bottom; consoles with tab
        tools_widget = QTabWidget()
        main_widget.addWidget(tools_widget)
        llm = LlmChat()
        console = Console()
        tools_widget.addTab(llm, 'LLM Chat')
        tools_widget.addTab(console, 'Console')
        self.tools = [llm, console]

        # left tree view
        tree_widget = QTabWidget()
        self.file_tree = FileTreeView(settings.install_dir)
        tree_widget.addTab(self.file_tree, 'Local Files')
        self.python_tree = PythonTree()
        self.python_tree.parse_python_code()
        tree_widget.addTab(self.python_tree, 'Python')
        top_splitter.addWidget(tree_widget)

        # text editor tabs
        right_top = QTabWidget()
        top_splitter.addWidget(right_top)
        self.editors = [PythonEditor()]
        for index, editor in enumerate(self.editors):
            right_top.addTab(editor, editor.tab_name)
            right_top.tabBar().setTabButton(index, QTabBar.ButtonPosition.RightSide, editor.get_tab_widget())

        self.setWindowTitle('Handy IDE')
        # first 2 values are x,y position in screen
        self.setGeometry(300, 100, DEFAULT_WINDOW_SIZE[0], DEFAULT_WINDOW_SIZE[1])

        # set ratios
        main_widget.setSizes([400, 200])
        top_splitter.setSizes([200, 600])

    def create_menu_and_toolbar(self):
        actions = get_all_actions(self)

        menu_bar = self.menuBar()
        for menu_name, entries in get_menu_setup(settings.gui_data).items():
            menu = menu_bar.addMenu(menu_name)
            for menu_entry in entries:
                if menu_entry == 'Seperator':
                    menu.addSeparator()
                else:
                    menu.addAction(actions[menu_entry])

        toolbar = self.addToolBar('Toolbar')
        for tool_action in get_toolbar_setup():
            toolbar.addAction(actions[tool_action])

    def open_file(self):
        filename, _ = QFileDialog.getOpenFileName(self, 'Open File', '', 'Text Files (*.txt)')
        if filename:
            with open(filename, 'r') as file:
                self.textEdit.setText(file.read())

    def save_file(self):
        filename, _ = QFileDialog.getSaveFileName(self, 'Save File', '', 'Text Files (*.txt)')
        if filename:
            with open(filename, 'w') as file:
                text = self.textEdit.toPlainText()
                file.write(text)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = TextEditor()
    ex.show()
    sys.exit(app.exec_())
