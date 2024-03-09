from handy.llm import Ollama

# simple example of chatting with an llm
# the llm will keep a record of the chat history


OLLAMA_MODEL = 'mistral:7b-instruct-v0.2-q8_0'


def chat_example_with_history():
    llm = Ollama(OLLAMA_MODEL)
    while True:
        request = input('> ')
        if request == 'exit':
            return
        llm.message_with_history(request)


if __name__ == '__main__':
    print('Enter your request for the llm and get the response.')
    chat_example_with_history()
