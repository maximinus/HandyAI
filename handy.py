import sys

from PyQt5.QtWidgets import (QApplication, QMainWindow, QTextEdit, QTreeView,
                             QSplitter, QTabWidget, QTabBar, QFileDialog)
from PyQt5.QtCore import Qt

from ide.settings import settings, get_all_actions, get_menu_setup, get_toolbar_setup
from ide.text_editor import PythonEditor


class TextEditor(QMainWindow):
    def __init__(self):
        super().__init__()
        self.create_menu_and_toolbar()

        main_split = QSplitter(Qt.Vertical)
        self.setCentralWidget(main_split)
        top_splitter = QSplitter(Qt.Horizontal)
        main_split.addWidget(top_splitter)

        # bottom; text with tabs
        bottom_widget = QTabWidget()
        main_split.addWidget(bottom_widget)
        bottom_widget.addTab(QTextEdit(), 'Tab 1')
        bottom_widget.addTab(QTextEdit(), 'Tab 2')

        # left tree view
        left_widget = QTabWidget()
        top_splitter.addWidget(left_widget)
        tree_view = QTreeView()
        left_widget.addTab(tree_view, 'Python')

        # text editor tabs
        right_top = QTabWidget()
        top_splitter.addWidget(right_top)
        self.editors = [PythonEditor()]
        for index, editor in enumerate(self.editors):
            right_top.addTab(editor, editor.tab_name)
            right_top.tabBar().setTabButton(index, QTabBar.ButtonPosition.RightSide, editor.get_tab_widget())

        self.setWindowTitle('Handy IDE')
        self.setGeometry(300, 100, 800, 600)

        # set ratios
        main_split.setSizes([400, 200])
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
