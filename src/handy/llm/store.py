import os.path
import sqlite3
from datetime import datetime

DATABASE_FILE = '~/.handy/chat_db.sqlite'


def make_tables(cursor):
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS chats (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            start_time TIMESTAMP NOT NULL,
            last_update TIMESTAMP NOT NULL
        )
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS exchanges (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            chat_id INTEGER NOT NULL,
            user_text TEXT NOT NULL,
            reply_text TEXT NOT NULL,
            timestamp TIMESTAMP NOT NULL,
            FOREIGN KEY (chat_id) REFERENCES chats (id)
        )
    ''')


class ChatDb:
    def __init__(self):
        build_tables = not os.path.exists(DATABASE_FILE)
        self.conn = sqlite3.connect(DATABASE_FILE)
        self.cursor = self.conn.cursor()
        if build_tables:
            make_tables(self.cursor)

    def use_memory(self):
        # mainly used for testing
        pass

    def add_exchange(self, chat_name, user_text, reply_text):
        self.cursor.execute('SELECT id FROM chats WHERE name = ?', (chat_name,))
        chat = self.cursor.fetchone()

        start_time = datetime.now()
        if chat is None:
            # no chat entry, update it
            last_update = start_time
            self.cursor.execute('''
                INSERT INTO chats (name, start_time, last_update)
                VALUES (?, ?, ?)''', (chat_name, start_time, last_update))
            self.conn.commit()
            chat_id = self.cursor.lastrowid
        else:
            chat_id = chat[0]

        self.cursor.execute('''
            INSERT INTO exchanges (chat_id, user_text, reply_text, timestamp)
            VALUES (?, ?, ?, ?)''', (chat_id, user_text, reply_text, start_time))
        self.cursor.execute('''
            UPDATE chats
            SET last_update_time = ?
            WHERE id = ?''', (start_time, chat_id))
        self.conn.commit()

    def get_chat_exchanges(self, chat_name):
        self.cursor.execute('SELECT id FROM chats WHERE name = ?', (chat_name,))
        chat = self.cursor.fetchone()
        if chat is None:
            return []

        chat_id = chat[0]
        self.cursor.execute('''
            SELECT user_text, reply_text FROM exchanges
            WHERE chat_id = ?
            ORDER BY timestamp ASC''', (chat_id,))
        return self.cursor.fetchall()

    def chat_exists(self, name):
        self.cursor.execute('SELECT 1 FROM chats WHERE name = ?', (name,))
        return self.cursor.fetchone() is not None


db = ChatDb()
