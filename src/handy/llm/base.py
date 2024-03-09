class SingleChat:
    def __init__(self, person, text):
        self.person = person
        self.text = text


class ChatResponse:
    def __init__(self, response):
        self.timestamp = response['created_at']
        self.text = response['response']
        self.error = False

    @classmethod
    def get_error_response(cls):
        response = cls({'created_at': '', 'response': 'Error'})
        response.error = True
        return response


class BaseLLM:
    def __init__(self):
        self.history = []

    def message(self, text: str) -> str:
        # pass a single message and get a single answer
        pass

    def message_with_history(self, text: str) -> str:
        # pass a single message with chat history
        pass

    def clear_history(self):
        # delete the entire history
        self.history = []
