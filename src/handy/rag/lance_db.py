import os
from tqdm import tqdm

import lancedb
from lancedb.embeddings import EmbeddingFunctionRegistry
from lancedb.db import LanceModel
from lancedb.pydantic import Vector

registry = EmbeddingFunctionRegistry.get_instance()
func = registry.get('sentence-transformers').create(device='cuda')

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
    # the sourcefield magic means this model handles converting text to vector automatically
    # so when we want to add to the table, we only need give it the string
    vector: Vector(func.ndims()) = func.VectorField()
    text: str = func.SourceField()


class LanceDB(BaseDB):
    def __init__(self):
        super().__init__()
        self.db = lancedb.connect(DATABASE_FILE)
        #self.table = self.db.create_table('texts', schema=LanceText)
        self.table = self.db.open_table('texts')

    def add_text(self, texts: list):
        for i in tqdm(texts):
            self.table.add([{'text': i}])

    def get_nearest_k(self, text: str, k: int):
        results = self.table.search(text).limit(k).to_pandas()
        return results


def add_folder_files_to_database(database, directory):
    all_chunks = process_directory(directory)
    database.add_text(all_chunks)


def split_text_into_chunks(text, chunk_size, overlap):
    chunks = []
    start = 0
    end = chunk_size
    while start < len(text):
        chunks.append(text[start:end])
        start = end - overlap
        end = start + chunk_size
    return chunks


def process_directory(directory):
    all_chunks = []
    for filename in tqdm(os.listdir(directory)):
        if filename.endswith('.txt'):
            file_path = os.path.join(directory, filename)
            with open(file_path, 'r', encoding='utf-8') as file:
                text = file.read()
                all_chunks.extend(split_text_into_chunks(text, 1000, 500))
    return all_chunks


if __name__ == '__main__':
    db = LanceDB()
    #add_folder_files_to_database(db, '/home/sparky/code/MistralTest/data/godot_docs/processed')
    foo = db.get_nearest_k('How to rotate a sprite', 5)
    print(foo)
