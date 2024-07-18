import ollama
from .base import BaseLLM, LLMResponse, LLMError


# TODO: difference between system, user or message?
# system: messages from the software, saying "do it like this"
# user: messages from the user
# message: ??
# https://github.com/ollama/ollama/issues/2217
#   Keep in mind that the MESSAGE commands only work with the /api/chat endpoint and do not work with /api/generate


class OllamaResponse(LLMResponse):
    def __next__(self):
        response = next(self.text_gen)
        # the response differs according to the type
        if 'message' in response:
            chunk = response['message']['content']
        else:
            chunk = response['response']
        self.tokens.append(chunk)
        return chunk


class Ollama(BaseLLM):
    def __init__(self, model_name: str):
        super().__init__()
        self.model_name = model_name

    def query(self, text: str) -> LLMResponse:
        try:
            return OllamaResponse(ollama.generate(model=self.model_name, prompt=text, stream=True))
        except (ollama.ResponseError, KeyError) as ex:
            raise LLMError(f'Error: {ex}')

    def get_history_in_ollama_format(self) -> list[dict]:
        self.convert_last()
        messages = []
        for i in self.history:
            messages.append({'role': 'user', 'content': i[0]})
            messages.append({'role': 'assistant', 'content': i[1]})
        return messages

    def chat(self, text: str) -> LLMResponse:
        all_chats = self.get_history_in_ollama_format()
        all_chats.append({'role': 'user', 'content': text})
        try:
            result = OllamaResponse(ollama.chat(model=self.model_name, messages=all_chats, stream=True))
            self.history.append([text, result])
            return result
        except ollama.ResponseError as ex:
            raise LLMError(f'Error: {ex}')

    def get_embedding(self, text):
        return ollama.embeddings(model=self.model_name, prompt=text)


def get_base_models():
    models = ollama.list()
    return [x['name'] for x in models['models']]
