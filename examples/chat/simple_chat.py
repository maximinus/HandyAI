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


test = """
You answer to this request can be either a answer OR a json structure.
I want to know the best Grateful Dead 1978 shows.
However, you may use an internet search to help you on this. If you return json like this:
{"name": "internet search", "search": "ENTER YOUR SEARCH HERE"}
Where you can change the uppercase inside the json to something else,
then you are using this the internet search tool.
To use the tool, you must only reply with the JSON and ABSOLUTELY NOTHING ELSE.
If you use this tool I will reply with the entire chat history as well as the information the tool provided,
which makes answering the question possible the next time we chat.
"""

test2= """
You used the internet search, which replied:
1: 24th June 1978, Oregon - Awesome Truckin' jam
2: 8th Feb, Washington DC - Killer Let It Grow > Space sequence
3: 31st Dec, Winterland, S.F. - Trippy Scarlet Fire
Either use the tool again or try to answer the question.
"""

test3="""
I have a task that needs doing by my team of workers.
I will describe the task, and I would like to give each worker a single job to do.
First my list of workers:
Peggy: Writes text content for websites
Mike: Codes websites
John: Manages servers and backends for websites
Lance: A graphic designer
The task is to make a beautiful website that has stories about ghosts.
Your response must be in the form of a json structure like this:
{"peggy": "???", "mike": "???", "john": "???", "lance": "???"}
But replace ??? with the task they should do.
You should only response with this JSON structure, and nothing else.
"""

llm = Ollama('mistral:7b-instruct-v0.2-q8_0')
history = []
while True:
    request = input('> ')
    if request == 'exit':
        break
    if request == 'test':
        print('Testing')
        request = test3
    if request == 'test2':
        print('Testing2')
        request = test2
    response = llm.message_with_history(request, history)
    history.append(response)
    print(response.get_text_response())
