import threading
import time

from PyQt5.QtWidgets import QTextEdit, QVBoxLayout, QLineEdit, QWidget
from PyQt5.QtCore import pyqtSignal, QObject
from PyQt5 import QtGui

from handy.llm.ollama_llm import Ollama


OUTPUT_COLOR = QtGui.QColor(0, 0, 128)
TOKEN_SLEEP_TIME = 0.1
# hack could be improved with slightly annoying code
END_MESSAGE_TOKEN = '%:%END_MESSAGE%:%'


class UpdateThread(QObject):
    update_signal = pyqtSignal(str)

    def run(self, chunked_answer):
        while True:
            next_tokens = chunked_answer.next()
            if next_tokens is None:
                # end of answer, we are complete
                self.update_signal.emit(END_MESSAGE_TOKEN)
                return
            self.update_signal.emit(next_tokens)
            time.sleep(0.05)


class LlmChat(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout()
        self.llm = Ollama('mistral:7b-instruct-v0.2-q8_0')
        self.chat_history = []
        self.input_locked = False
        self.display = QTextEdit()
        self.display.setReadOnly(True)
        self.user_entry = QLineEdit()
        layout.addWidget(self.display)
        layout.addWidget(self.user_entry)
        self.user_entry.returnPressed.connect(self.user_entered_request)
        self.user_entry.setPlaceholderText('Ask the LLM')
        self.setLayout(layout)
        self.update_worker = UpdateThread()
        self.thread = None
        self.update_worker.update_signal.connect(self.update_text)

    def user_entered_request(self):
        request = self.user_entry.text()
        self.user_entry.clear()
        self.user_entry.setEnabled(False)
        self.add_llm_message(f'You: {request}')
        self.send_request(request)

    def update_text(self, text):
        # updates from the response thread
        if text == END_MESSAGE_TOKEN:
            # end of generation, thread will also finish after this
            self.add_llm_message('\n', response=True, line_feed=False)
            self.user_entry.setEnabled(True)
        else:
            self.add_llm_message(text, response=True, line_feed=False)

    def add_llm_message(self, message, response=False, line_feed=True):
        cursor = self.display.textCursor()
        if response:
            text_format = QtGui.QTextCharFormat()
            text_format.setFontItalic(True)
            text_format.setForeground(QtGui.QBrush(OUTPUT_COLOR))
            cursor.setCharFormat(text_format)
        if line_feed is True:
            cursor.insertText(f'{message}\n')
        else:
            cursor.insertText(message)
        cursor.setCharFormat(QtGui.QTextCharFormat())
        self.display.setTextCursor(cursor)

    def send_request(self, request):
        response = self.llm.message_with_history_streaming(request, self.chat_history)
        #self.history.append(response)
        # TODO: cut history if too long
        # response is a generator, we start the thread with it
        self.thread = threading.Thread(target=self.update_worker.run, args=(response,))
        self.thread.start()
