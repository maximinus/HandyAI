import ast

from PyQt5.QtWidgets import QTreeView
from PyQt5.QtGui import QStandardItemModel, QStandardItem


example_code = """
def add(a, b):
    return a + b

def sub(a, b):
    return a - b

foo = 5
""".strip()


class PythonTree(QTreeView):
    def __init__(self):
        super().__init__()
        self.python_model = QStandardItemModel()
        self.python_model.setHorizontalHeaderLabels(['AST Node', 'Details'])
        self.setModel(self.python_model)

    def parse_python_code(self, code=example_code):
        tree = ast.parse(code)
        self.add_ast_nodes(None, tree)

    def add_ast_nodes(self, parent, node):
        if parent is None:
            parent = self.python_model.invisibleRootItem()
        item = QStandardItem(node.__class__.__name__)
        details = ', '.join(f'{key}={value}' for key, value in ast.iter_fields(node) if not isinstance(value, ast.AST))
        details_item = QStandardItem(details)
        parent.appendRow([item, details_item])
        for child in ast.iter_child_nodes(node):
            self.add_ast_nodes(item, child)
