import unittest

from handy.llm.base import Exchange, Message
from handy.llm.ollama_llm import Ollama


class TestOllamaBase(unittest.TestCase):
    def test_get_history(self):
        # check no error here
        message1 = Message(text='test')
        message2 = Message(text='test')
        chats = [Exchange(message1, message2)]
        ollama = Ollama('test')
        ollama.get_history_in_ollama_format(chats)
