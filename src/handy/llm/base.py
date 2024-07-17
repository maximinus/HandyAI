from handy.llm.store import db, generate_unique_name


class LLMError(Exception):
    pass


class LLMChatExists(LLMError):
    pass


class LLMResponse:
    def __init__(self, text_gen):
        self.text_gen = text_gen
        self.tokens = []

    def __iter__(self):
        return self

    def __next__(self):
        raise StopIteration

    @property
    def response(self):
        for i in self:
            pass
        return ''.join(self.tokens)


class BaseLLM:
    def __init__(self):
        self.history = []
        self.store_name = None

    def query(self, text: str) -> LLMResponse:
        # pass a single message and get a response
        return LLMResponse(None)

    def chat(self, text: str) -> LLMResponse:
        # pass a single message with chat history
        self.history.append([text, ''])
        return LLMResponse(None)

    def clear_history(self):
        # delete the entire history
        self.history = []
        if self.store_name is not None:
            db.clear_chat_history(self.store_name)

    def convert_last(self):
        # the last history one may be a chunked response, if so replace with the data
        if len(self.history) > 0:
            if isinstance(self.history[-1][1], LLMResponse):
                self.history[-1][1] = self.history[-1][1].response
            # and store in the db if needed
            if self.store_name is not None:
                db.add_exchange(self.store_name, self.history[-1][0], self.history[-1][1])

    def __del__(self):
        # maybe the last history was not saved, check here
        self.convert_last()

    def use_store(self, name=None):
        # if the name exists, update with a new one
        if name is None:
            name = generate_unique_name()
        # if the name exists AND we have history, we have an issue
        self.store_name = name
        if db.chat_exists(name):
            if len(self.history) > 0:
                raise LLMChatExists('Cannot use store at it exists already and we have chat history')
            else:
                self.history = db.get_chat_exchanges(self.store_name)
        else:
            if len(self.history) > 0:
                # write this to the db
                for exchange in self.history:
                    db.add_exchange(self.store_name, exchange[0], exchange[1])

