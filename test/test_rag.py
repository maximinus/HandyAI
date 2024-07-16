import unittest

from handy.rag.lance_db import LanceDB


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
