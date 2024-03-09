from handy.llm import Ollama

# simple example of sending the llm a single request and printing the response
# you may change the model if you like

OLLAMA_MODEL = 'mistral:7b-instruct-v0.2-q8_0'


def single_chat_example():
    llm = Ollama(OLLAMA_MODEL)
    response = llm.message('How big is the moon?')
    print(response.text)


if __name__ == '__main__':
    single_chat_example()
