from datetime import datetime


class SingleChat:
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


class SingleQuery:
    """
    A request and it's response
    """
    def __init__(self, request: SingleChat, response: SingleChat):
        self.request = request
        self.response = response
        self.error = False

    def get_text_response(self) -> str:
        return self.response.text

    @classmethod
    def get_error(cls, request, error_text):
        query = SingleQuery(request, error_text)
        query.error = True
        return query


class BaseLLM:
    def __init__(self):
        self.history = []

    def message(self, text: str) -> SingleChat:
        # pass a single message and get a single answer
        return SingleChat.get_error()

    def message_with_history(self, text: str) -> SingleChat:
        # pass a single message with chat history
        return SingleChat.get_error()

    def clear_history(self):
        # delete the entire history
        self.history = []
