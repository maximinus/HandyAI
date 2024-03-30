import sys

from PyQt5.QtWidgets import QApplication, QMainWindow, QSplitter, QTabWidget, QAction
from PyQt5.QtCore import Qt

from ide.settings import settings, SettingsWindow, get_icon
from ide.text_editor import TextEditorContainer
from ide.file_tree import FileTreeView
from ide.python_tree import PythonTree
from ide.llm_chat import LlmChat
from ide.python_repl import PythonREPL
from ide.searchbox import add_search


DEFAULT_WINDOW_SIZE = [1024, 768]
# this is based on the height
MAIN_WIDGET_RATIO = [568, 200]
# and then the width
SUB_WIDGET_RATIO = [300, 724]


def get_action(icon, text, window, callback):
    if icon is not None:
        action = QAction(get_icon(icon), text, window)
    else:
        action = QAction(text, window)
    action.triggered.connect(callback)
    return action


class HandyIDE(QMainWindow):
    def __init__(self):
        super().__init__()
        self.text_editors = TextEditorContainer()
        self.create_menu_and_toolbar()

        main_widget = QSplitter(Qt.Vertical)
        self.setCentralWidget(main_widget)
        top_splitter = QSplitter(Qt.Horizontal)
        main_widget.addWidget(top_splitter)

        # bottom; consoles with tab
        tools_widget = QTabWidget()
        main_widget.addWidget(tools_widget)
        llm = LlmChat()
        repl = PythonREPL()
        tools_widget.addTab(llm, 'LLM Chat')
        tools_widget.addTab(repl, 'Console')
        self.tools = [llm, repl]

        # left tree view
        tree_widget = QTabWidget()
        self.file_tree = FileTreeView(settings.install_dir)
        tree_widget.addTab(self.file_tree, 'Local Files')
        self.python_tree = PythonTree()
        self.python_tree.parse_python_code()
        tree_widget.addTab(self.python_tree, 'Python')
        top_splitter.addWidget(tree_widget)

        # text editor tabs
        top_splitter.addWidget(self.text_editors)

        self.setWindowTitle('Handy IDE')
        # first 2 values are x,y position in screen
        self.setGeometry(300, 100, DEFAULT_WINDOW_SIZE[0], DEFAULT_WINDOW_SIZE[1])

        # set ratios
        main_widget.setSizes([400, 200])
        top_splitter.setSizes([200, 600])

    def not_implemented(self):
        raise NotImplementedError

    def create_menu_and_toolbar(self):
        actions = {'open': get_action('open', 'Open', self, self.text_editors.open_file),
                   'new-file': get_action('new-file', 'New', self, self.text_editors.new_file),
                   'settings': get_action('settings', 'Settings', self, self.not_implemented),
                   'exit-handy': get_action('exit', 'Exit', self, self.not_implemented),
                   'cut-text': get_action('cut', 'Cut', self, self.text_editors.cut_text),
                   'copy-text': get_action('copy', 'Copy', self, self.text_editors.copy_text),
                   'paste-text': get_action('copy-paste', 'Paste', self, self.text_editors.paste_text),
                   'delete-text': get_action('delete', 'Delete', self, self.text_editors.delete_text),
                   'help-handy': get_action('help', 'Help', self, self.not_implemented),
                   'about-handy': get_action('info', 'About', self, self.not_implemented)}

        menu_bar = self.menuBar()
        menu = menu_bar.addMenu('File')
        menu.addAction(actions['new-file'])
        menu.addAction(actions['open'])
        menu.addSeparator()
        menu.addAction(actions['settings'])
        menu.addSeparator()
        menu.addAction(actions['exit-handy'])

        menu = menu_bar.addMenu('Edit')
        menu.addAction(actions['cut-text'])
        menu.addAction(actions['copy-text'])
        menu.addAction(actions['paste-text'])
        menu.addAction(actions['delete-text'])

        menu = menu_bar.addMenu('Help')
        menu.addAction(actions['help-handy'])
        menu.addAction(actions['about-handy'])

        toolbar = self.addToolBar('Toolbar')
        toolbar.addAction(actions['new-file'])
        toolbar.addAction(actions['open'])
        toolbar.addAction(actions['help-handy'])

        add_search(toolbar)

    def show_options(self):
        settings = SettingsWindow(self)
        settings.setModal(True)
        settings.exec_()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = HandyIDE()
    ex.show()
    sys.exit(app.exec_())
