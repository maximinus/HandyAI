from datetime import datetime


class Message:
    """
    Some text either sent to something (was_response=False), or received (was_response=True)
    """
    def __init__(self, user: str = '', text: str = '', timestamp: datetime|None = None, was_response=False):
        self.user = user
        self.text = text
        self.timestamp = timestamp
        self.was_response = was_response
        self.error = False

    @classmethod
    def get_error(cls, was_response=False):
        response = cls(was_response=was_response)
        response.error = True
        return response


class Exchange:
    """
    A request and it's response
    """
    def __init__(self, request: Message, response: Message):
        self.request = request
        self.response = response
        self.error = False

    def get_text_response(self) -> str:
        return self.response.text

    @classmethod
    def get_error(cls, request, error_text):
        query = Exchange(request, error_text)
        query.error = True
        return query

    @classmethod
    def from_text(cls, user_text, response_text):
        user_chat = Message(text=user_text)
        response_chat = Message(text=response_text, was_response=True)
        return cls(user_chat, response_chat)


class BaseLLM:
    def __init__(self):
        self.history = []

    def message(self, text: str) -> Message:
        # pass a single message and get a single answer
        return Message.get_error()

    def message_with_history(self, text: str) -> Message:
        # pass a single message with chat history
        return Message.get_error()

    def clear_history(self):
        # delete the entire history
        self.history = []
