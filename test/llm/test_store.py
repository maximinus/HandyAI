import sqlite3
import unittest


class TestChatDatabase(unittest.TestCase):
    def setUp(self):
        # Create an in-memory SQLite database
        self.conn = sqlite3.connect(':memory:')
        self.cursor = self.conn.cursor()

        # Create the tables
        self.cursor.execute('''
        CREATE TABLE chats (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            start_time TIMESTAMP NOT NULL,
            last_update_time TIMESTAMP NOT NULL
        )
        ''')

        self.cursor.execute('''
        CREATE TABLE exchanges (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            chat_id INTEGER NOT NULL,
            user_text TEXT NOT NULL,
            reply_text TEXT NOT NULL,
            timestamp TIMESTAMP NOT NULL,
            FOREIGN KEY (chat_id) REFERENCES chats (id)
        )
        ''')
        self.conn.commit()

    def tearDown(self):
        # Close the connection after each test
        self.conn.close()

    def test_add_exchange_creates_chat_if_not_exists(self):
        add_exchange('Chat 1', 'Hello!', 'Hi there!', self.cursor, self.conn)
        self.cursor.execute('SELECT * FROM chats WHERE name = "Chat 1"')
        chat = self.cursor.fetchone()
        self.assertIsNotNone(chat)
        self.assertEqual(chat[1], 'Chat 1')

    def test_add_exchange_adds_to_existing_chat(self):
        create_chat('Chat 1', self.cursor, self.conn)
        add_exchange('Chat 1', 'Hello!', 'Hi there!', self.cursor, self.conn)
        exchanges = get_chat_exchanges('Chat 1', self.cursor)
        self.assertEqual(len(exchanges), 1)
        self.assertEqual(exchanges[0], ('Hello!', 'Hi there!'))

    def test_get_chat_exchanges(self):
        create_chat('Chat 1', self.cursor, self.conn)
        add_exchange('Chat 1', 'Hello!', 'Hi there!', self.cursor, self.conn)
        add_exchange('Chat 1', 'How are you?', 'I am fine, thank you.', self.cursor, self.conn)
        exchanges = get_chat_exchanges('Chat 1', self.cursor)
        self.assertEqual(len(exchanges), 2)
        self.assertEqual(exchanges[0], ('Hello!', 'Hi there!'))
        self.assertEqual(exchanges[1], ('How are you?', 'I am fine, thank you.'))

    def test_chat_exists(self):
        create_chat('Chat 1', self.cursor, self.conn)
        self.assertTrue(chat_exists('Chat 1', self.cursor))
        self.assertFalse(chat_exists('Nonexistent Chat', self.cursor))
