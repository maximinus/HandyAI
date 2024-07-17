import unittest

from handy.llm.ollama_llm import Ollama, OllamaResponse


class DummyIterator:
    def __init__(self, size):
        self.size = size
        self.count = 1

    def __iter__(self):
        return self

    def __next__(self):
        if self.count <= self.size:
            current = {'message': {'content': str(self.count)}}
            self.count += 1
            return current
        else:
            raise StopIteration


class TestResponse(unittest.TestCase):
    def test_simple_response(self):
        response = OllamaResponse(DummyIterator(5))
        self.assertEqual(response.response, '12345')

    def test_single_response(self):
        results = [str(x + 1) for x in range(5)]
        response = OllamaResponse(DummyIterator(5))
        for index, value in enumerate(response):
            self.assertEqual(results[index], value)

    def test_interruption(self):
        response = OllamaResponse(DummyIterator(5))
        response.__next__()
        response.__next__()
        self.assertEqual(response.response, '12345')
