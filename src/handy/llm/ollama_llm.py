import ollama
from handy.logger.output import logger
from .base import SingleChat, BaseLLM

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

    def message(self, text: str) -> SingleChat:
        try:
            result = ollama.generate(model=self.model_name, prompt=text)
            return SingleChat(result)
        except ollama.ResponseError as ex:
            logger.error(f'Ollama error: {ex}')

    def get_history_in_ollama_format(self) -> list[dict]:
        return [{'role': x.user, 'content': x.text} for x in self.history]

    def message_with_history(self, text: str) -> SingleChat:
        try:
            # we have to send the history as well
            all_chats = self.get_history_in_ollama_format()
            all_chats.append({'role': 'user', 'content': text})
            result = ollama.chat(model=self.model_name, messages=all_chats)
            # it worked, so store the history
            self.history.append(SingleChat(user='user', text=text, timestamp=datetime.now()))
            response = SingleChat(user=result['message']['role'],
                                  text=result['message']['content'],
                                  timestamp=datetime.now(),
                                  was_response=True)
            self.history.append(response)
            return response
        except ollama.ResponseError as ex:
            logger.error(f'Ollama error: {ex}')
