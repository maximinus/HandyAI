import unittest

from handy.llm import db


class TestChatDatabase(unittest.TestCase):
    def setUp(self):
        # this also deletes all the data in-memory
        db.use_memory()

    def test_add_exchange_creates_chat_if_not_exists(self):
        db.add_exchange('Chat 1', 'Hello!', 'Hi there!')
        db.cursor.execute('SELECT * FROM chats WHERE name = "Chat 1"')
        chat = db.cursor.fetchone()
        self.assertIsNotNone(chat)
        self.assertEqual(chat[1], 'Chat 1')

    def test_add_exchange_adds_to_existing_chat(self):
        db.create_chat('Chat 1')
        db.add_exchange('Chat 1', 'Hello!', 'Hi there!')
        exchanges = db.get_chat_exchanges('Chat 1')
        self.assertEqual(len(exchanges), 1)
        self.assertEqual(exchanges[0], ('Hello!', 'Hi there!'))

    def test_get_chat_exchanges(self):
        db.create_chat('Chat 1')
        db.add_exchange('Chat 1', 'Hello!', 'Hi there!')
        db.add_exchange('Chat 1', 'How are you?', 'I am fine, thank you.')
        exchanges = db.get_chat_exchanges('Chat 1')
        self.assertEqual(len(exchanges), 2)
        self.assertEqual(exchanges[0], ('Hello!', 'Hi there!'))
        self.assertEqual(exchanges[1], ('How are you?', 'I am fine, thank you.'))

    def test_chat_exists(self):
        db.create_chat('Chat 1', self.cursor, self.conn)
        self.assertTrue(db.chat_exists('Chat 1'))
        self.assertFalse(db.chat_exists('Nonexistent Chat'))
