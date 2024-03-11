from handy.llm.ollama_llm import Ollama
from handy.tools.simple_tool import Tool

# for this simple test, we want to do the following:
# we send an instruction to the llm asking it to send back a json structure
# we then test wether that happened or not.
# the possibilities are (from worst to best)
# 1: The response was not json
# 2: The response was json but did not match a tool
# 3: The response was json and matched a tool

example_argument = """
Your answer to this request MUST be a valid json string, in one of the formats specified below.
There are %total% different tools you can use to help in solving my problem.
I will now describe the tools and the json response they require:
%tools%
Or you can return the answer to the question below. To do this, return json like {"answer": "SOME_TEXT"}
For these tools, replace SOME_TEXT or SOME_NUMBER with your own values.
If you use a tool I will reply with the entire chat history as well as the information the tool provided,
which makes answering the question possible the next time we chat.
The question I would like answered is: %question%
Remember, you must answer ONLY with valid json, and nothing else.
"""

best_shows = """
Internet search replied
1: 24th June 1978, Oregon - Awesome Truckin' jam
2: 8th Feb, Washington DC - Killer Let It Grow > Space sequence
3: 31st Dec, Winterland, S.F. - Trippy Scarlet Fire

If you wish to return an answer, you must reply with this json format:
{"answer": "SOME_TEXT"}
And replace SOME_TEXT with your answer
"""


def internet(search_text: str):
    """
    A tool to search the internet with Google.
    """
    pass


def time_now():
    """
    A tool to return the current time.
    """
    pass


def test_function_call():
    internet_tool = Tool(internet)
    time_tool = Tool(time_now)
    tool_texts = []
    for index, i in enumerate([internet_tool, time_tool]):
        tool_texts.append(f'{index + 1}: {str(i)}')
    desc = '\n'.join(tool_texts)
    request = example_argument
    request = request.replace('%total%', '2')
    request = request.replace('%tools%',desc)
    request = request.replace('%question%', 'What are the best Grateful Dead shows?')

    llm = Ollama('mistral:7b-instruct-v0.2-q8_0')
    history = [llm.message_with_history(request)]
    response = llm.message_with_history(best_shows, history)
    print(response.get_text_response())


if __name__ == '__main__':
    test_function_call()
