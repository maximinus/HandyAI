import unittest

from handy.rag.lance_db import LanceDB
from handy.llm import Ollama


class TestLLMEmbedding(unittest.TestCase):
    def test_can_get_embedding(self):
        llm = Ollama('mistral:latest')
        result = llm.get_embedding('This is a test')
        self.assertIsNotNone(result)


class TestLanceRag(unittest.TestCase):
    def setUp(self):
        self.db = LanceDB()

    def test_insert_data(self):
        # we can add data to a store
        pass

    def test_insert_data_no_store(self):
        pass

    def test_get_stores(self):
        # we can see all stores
        pass

    def test_delete_store(self):
        pass

    def test_get_nearest(self):
        pass
