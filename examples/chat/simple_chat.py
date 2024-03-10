from handy.llm.ollama_llm import Ollama

# simple example of chatting with an llm
# the llm will keep a record of the chat history

"""
Based on early results, we should ask for a json tool output at all times.
It should be an error to not output json.
Every json tool should look the same, to make it easy
{'name': 'string', data: 'string'}
One reply is "answer"

So therefore we list a number of tools and given a problem ask the agent to use a tool.
If the response does not send back valid json, maybe try increasing the temperature.
"""

llm = Ollama('mistral:7b-instruct-v0.2-q8_0')
history = []
while True:
    request = input('> ')
    if request == 'exit':
        break
    response = llm.message_with_history(request, history)
    history.append(response)
    print(response.get_text_response())
