# used to test the functionality

from llm.ollama import Ollama

OLLAMA_MODEL = 'mistral:7b-instruct-v0.2-q8_0'


def single_chat_example():
    llm = Ollama(OLLAMA_MODEL)
    response = llm.message('How high should a mountain be?')
    print(response.text)


def chat_example_with_history():
    llm = Ollama(OLLAMA_MODEL)
    while True:
        request = input('> ')
        if request == 'exit':
            return
        llm.message_with_history(request)


if __name__ == '__main__':
    chat_example_with_history()
