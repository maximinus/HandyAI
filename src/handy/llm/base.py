class LLMError(Exception):
    pass


class LLMResponse:
    def __init__(self, text_gen):
        self.text_gen = text_gen
        self.tokens = []

    def __iter__(self):
        return self

    def __next__(self):
        response = next(self.text_gen)
        chunk = response['message']['content']
        self.tokens.append(chunk)
        return chunk

    @property
    def response(self):
        for i in self:
            pass
        return ''.join(self.tokens)


class BaseLLM:
    def __init__(self):
        self.history = []

    def query(self, text: str) -> LLMResponse:
        # pass a single message and get a response
        return ''

    def chat(self, text: str) -> LLMResponse:
        # pass a single message with chat history
        self.history.append([text, ''])
        return ''

    def clear_history(self):
        # delete the entire history
        self.history = []
