import ollama
from .base import SingleChat, SingleQuery, BaseLLM

from datetime import datetime

# TODO: difference between system, user or message?
# system: messages from the software, saying "do it like this"
# user: messages from the user
# message: ??
# https://github.com/ollama/ollama/issues/2217
#   Keep in mind that the MESSAGE commands only work with the /api/chat endpoint and do not work with /api/generate


class ChunkedAnswer:
    def __init__(self, request, text_gen, model_name):
        self.model_name = model_name
        self.request = SingleChat(user='user', text=request, timestamp=datetime.now())
        self.history = []
        self.text_gen = text_gen

    @property
    def valid(self):
        return self.text_gen is not None

    def next(self):
        try:
            next_response = next(self.text_gen)
            tokens = next_response['message']['content']
            self.history.append(tokens)
            return tokens
        except StopIteration:
            # we've finished
            return None

    def get_single_query(self):
        all_tokens = ' '.join(self.history)
        response = SingleChat(user=self.model_name,
                              text=all_tokens,
                              timestamp=datetime.now(),
                              was_response=True)
        return SingleQuery(self.request, response)


class Ollama(BaseLLM):
    def __init__(self, model_name: str):
        super().__init__()
        self.model_name = model_name

    def message(self, text: str) -> SingleQuery:
        request = SingleChat(user='user', text=text, timestamp=datetime.now())
        try:
            result = ollama.generate(model=self.model_name, prompt=text)
            response = SingleChat(user=self.model_name,
                                  text=result['response'],
                                  timestamp=datetime.now(),
                                  was_response=True)
            return SingleQuery(request, response)
        except ollama.ResponseError as ex:
            return SingleQuery.get_error(request, f'Ollama error: {ex}')

    def message_streaming(self, text: str) -> ChunkedAnswer:
        try:
            response = ollama.generate(model=self.model_name, prompt=text, stream=True)
        except ollama.ResponseError as ex:
            return ChunkedAnswer(f'Error: {ex}', None, self.model_name)
        return ChunkedAnswer(text, response, self.model_name)

    def get_history_in_ollama_format(self, history: list[SingleQuery]) -> list[dict]:
        messages = []
        for i in history:
            messages.append({'role': i.request.user, 'content': i.request.text})
            messages.append({'role': i.response.user, 'content': i.response.text})
        return messages

    def message_with_history(self, text: str, history: list[SingleQuery] | None = None) -> SingleQuery:
        all_chats = []
        if history is not None:
            all_chats = self.get_history_in_ollama_format(history)
        # add the current message
        all_chats.append({'role': 'user', 'content': text})
        request = SingleChat(user='user', text=text, timestamp=datetime.now())
        try:
            result = ollama.chat(model=self.model_name, messages=all_chats)
            response = SingleChat(user=result['message']['role'],
                                  text=result['message']['content'],
                                  timestamp=datetime.now(),
                                  was_response=True)
            return SingleQuery(request, response)
        except ollama.ResponseError as ex:
            return SingleQuery.get_error(request, f'Ollama error: {ex}')

    def message_with_history_streaming(self, text: str, history: list[SingleQuery] | None = None) -> ChunkedAnswer:
        all_chats = []
        if history is not None:
            all_chats = self.get_history_in_ollama_format(history)
        # add the current message
        all_chats.append({'role': 'user', 'content': text})
        try:
            result = ollama.chat(model=self.model_name, messages=all_chats, stream=True)
            return ChunkedAnswer(text, result, self.model_name)
        except ollama.ResponseError as ex:
            return ChunkedAnswer(f'Error: {ex}', None, self.model_name)

    def message_with_tools(self, text, tools, show_history=False) -> SingleQuery:
        # we do the following:
        # set the format option to json, to force a json response
        # set the system message to show tool usage
        # context, if there is history
        pass


def get_base_models():
    models = ollama.list()
    return [x['name'] for x in models['models']]
