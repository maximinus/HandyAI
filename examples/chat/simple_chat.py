from handy.llm.ollama_llm import Ollama

# simple example of chatting with an llm
# the llm will keep a record of the chat history

llm = Ollama('mistral:7b-instruct-v0.2-q8_0')
history = []
while True:
    request = input('> ')
    if request == 'exit':
        break
    response = llm.message_with_history(request, history)
    history.append(response)
    print(response.get_text_response())
