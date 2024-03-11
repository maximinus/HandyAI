import lancedb
from lancedb.embeddings import EmbeddingFunctionRegistry
from lancedb.db import LanceModel
from lancedb.pydantic import Vector

registry = EmbeddingFunctionRegistry.get_instance()
func = registry.get('sentence-transformers').create(device='gpu')

# we need a base system that others use

DATABASE_FILE = '~/.handy/handy-db'


class BaseDB:
    def __init__(self):
        pass

    def add_text(self, texts: list):
        pass

    def get_top_k(self, k) -> list:
        return []


class LanceText(LanceModel):
    text: str = func.SourceField()
    vector: Vector(func.ndims()) = func.VectorField()


class LanceDB(BaseDB):
    def __init__(self):
        super().__init__()
        self.db = lancedb.connect(DATABASE_FILE)
        self.table = self.db.create_table('texts', schema=LanceText())

    def add_text(self, texts: list):
        pass

    def get_nearest_k(self, text: str, k: int) -> list:
        return []


if __name__ == '__main__':
    db = LanceDB()
    db.add_text(['Hello, World!'])
    print(db.get_nearest_k(1), 'Hello everyone!')
