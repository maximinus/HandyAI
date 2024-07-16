from handy.llm.ollama_llm import Ollama

LLM_MODEL = 'mistral:latest'

llm = Ollama(LLM_MODEL)
history = []
while True:
    request = input('> ')
    if request == 'exit':
        break
    response = llm.message_with_history(request, history)
    history.append(response)
    print(response.get_text_response())
