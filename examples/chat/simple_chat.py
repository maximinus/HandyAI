from handy.llm.ollama_llm import Ollama

LLM_MODEL = 'mistral:latest'

llm = Ollama(LLM_MODEL)

while True:
    request = input('\n> ')
    if request == 'exit':
        break
    response = llm.chat(request)
    for chunk in response:
        print(chunk, end='')
