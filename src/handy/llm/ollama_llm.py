import ollama
from handy.logger.output import logger
from .base import SingleChat, SingleQuery, BaseLLM

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
            logger.error(f'Ollama error: {ex}')
        return SingleQuery(request, SingleChat.get_error(was_response=True))

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
        print(all_chats)
        request = SingleChat(user='user', text=text, timestamp=datetime.now())
        try:
            result = ollama.chat(model=self.model_name, messages=all_chats)
            response = SingleChat(user=result['message']['role'],
                                  text=result['message']['content'],
                                  timestamp=datetime.now(),
                                  was_response=True)
            return SingleQuery(request, response)
        except ollama.ResponseError as ex:
            logger.error(f'Ollama error: {ex}')
        return SingleQuery(request, SingleChat.get_error(was_response=True))

    def message_with_tools(self, text, tools, show_history=False) -> SingleQuery:
        # we do the following:
        # set the format option to json, to force a json response
        # set the system message to show tool usage
        # context, if there is history
        pass
