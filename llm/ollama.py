import ollama


class ChatHistory:
    def __init__(self, request, reply):
        self.request = request
        self.reply = reply


class BaseLLM:
    def __init__(self):
        self.history = []

    def message(self, request: str) -> str:
        # pass a single message and get a single answer
        pass

    def message_with_history(self, request: str) -> str:
        # pass a single message with chat history
        pass

    def clear_history(self):
        self.history = []

    def set_history(self, new_history: ChatHistory):
        self.history.append(new_history)


# required:
# single shot message
# message with conversation history
# TODO: difference between system, user or message?


class Ollama(BaseLLM):
    def __init__(self, model_name: str):
        super().__init__(self)
        self.model_name = model_name

    def message(self, text: str) -> str:
        try:
            result = ollama.generate(model=self.model_name, prompt=text)
        except ollama.ResponseError as ex:
            log()
        print(result)
