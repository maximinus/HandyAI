from typing import Callable

# router passes messages from object A to object B


class Message:
    def __init__(self, name: str, data: dict):
        self.name = name
        self.data = data


class Handler:
    def __init__(self, name: str, callback: Callable, message_names: list):
        self.name = name
        self.callback = callback
        self.message_names = message_names

    def handle_message(self, message: Message):
        # returns True if message to be stopped here
        # the callback may also return False
        if message.name not in self.message_names:
            return False
        return self.callback(message)


class Router:
    def __init__(self):
        self.handlers = []

    def send(self, message: Message):
        for handler in self.handlers:
            if handler.handle_message(message):
                return


router = Router()
