from PyQt5.QtWidgets import QFileSystemModel, QTreeView


class FileTreeView(QTreeView):
    def __init__(self, rootpath):
        super().__init__()
        self.files_model = QFileSystemModel()
        self.root_directory = str(rootpath)
        self.files_model.setRootPath(self.root_directory)
        self.setModel(self.files_model)
        self.setRootIndex(self.files_model.index(self.root_directory))
        self.setColumnHidden(1, True)
        self.setColumnHidden(2, True)
        self.setColumnHidden(3, True)
