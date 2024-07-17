import ollama
from .base import BaseLLM, LLMResponse, LLMError

from datetime import datetime

# TODO: difference between system, user or message?
# system: messages from the software, saying "do it like this"
# user: messages from the user
# message: ??
# https://github.com/ollama/ollama/issues/2217
#   Keep in mind that the MESSAGE commands only work with the /api/chat endpoint and do not work with /api/generate


class Ollama(BaseLLM):
    def __init__(self, model_name: str):
        super().__init__()
        self.model_name = model_name

    def query(self, text: str) -> LLMResponse:
        try:
            return LLMResponse(ollama.generate(model=self.model_name, prompt=text, stream=True))
        except (ollama.ResponseError, KeyError) as ex:
            raise LLMError(f'Error: {ex}')

    def get_history_in_ollama_format(self) -> list[dict]:
        if len(self.history) > 0:
            # the last one may be a chunked response, if so deal with it
            if isinstance(self.history[-1][1], LLMResponse):
                self.history[-1][1] = self.history[-1][1].response
        messages = []
        for i in self.history:
            messages.append({'role': 'user', 'content': i[0]})
            messages.append({'role': 'ai', 'content': i[1]})
        return messages

    def chat(self, text: str) -> str:
        all_chats = self.get_history_in_ollama_format()
        all_chats.append({'role': 'user', 'content': text})
        try:
            result = LLMResponse(ollama.chat(model=self.model_name, messages=all_chats))
            self.history.append([text, result])
            return result
        except ollama.ResponseError as ex:
            raise LLMError(f'Error: {ex}')


def get_base_models():
    models = ollama.list()
    return [x['name'] for x in models['models']]
