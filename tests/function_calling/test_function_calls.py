import ollama
import inspect
from typing import Callable


# function calling with local llm

# There are several parts to this
# First, we need to define what "function calling" is.
# We can define it as a 2 step process:
#   1: We give an llm a system prompt that describes a number of tools than can be used by returning some json
#   2: If the json returned is correct, then we run that tool and return the contents of that tool to the llm.
#
# Now let's break that down even more
# A tool needs to be defined in some way. We will define it as a python function
# The python function will always return some string
# We need to build up the description of the function and turn it into a json object
# To do this, weneed to imagine what it is we actually want to pass to the llm.
# Let's imagine a google search. All we need is some text to search
# To differentiate between different tools, we also need a tool name.
# So the json we would like to see returned is something like this:
#
# {"tool": "google_search", "search_text": "How to cook fried eggs"}
#
# And what we actually have is something like this:
#
# def google_search(search_text: str) -> str:
#     return do_the_search(search_text)
#
# However, to pass the json we likely need to describe what it that the llm needs to give us.
# The easiest place to do this is in the docstring, however, we will need to pull it out manually
# Let's add a docstring like this:
#
# def google_search(search_text: str) -> str:
#     """
#     Use google to search the internet to find out about a subject.
#
#     search_text: The subject to search about.
#     """
#
# And from this, we need to describe the tool to the llm. So we would like to create this:
# Use google to search the internet to find out about a subject. To use, return json in the format {"tool": "google_search", "search_text": "The subject to search about."}.
#
# Next, we need to describe how to reply using the tools.
# We do this by prompt engineering, and being explicit about what we want done.
#
# Now the hard bit. We need to work out what we want to do.
# So, for example, I want a program that can do X.
# At the moment, we can only really do functional programs.

class Tool:
    def __init__(self, func: Callable):
        self.function = func
        self.description, self.args = self.get_description_and_args(func.__doc__)
        self.name = func.__name__

    def get_description_and_args(self, docstring):
        args = self.get_all_args()
        description = []
        text = []
        for line in docstring.strip().splitlines():
            filtered_line = line.strip()
            if len(filtered_line) == 0:
                continue
            data = filtered_line.split(':')
            if len(data) > 1 and data[0] in args:
                text.append(f'"{data[0]}": {args[data[0]].replace("%%description%%", data[1].strip())}')
            else:
                description.append(filtered_line)
        return ''.join(description), text

    def get_all_args(self):
        signature = inspect.signature(self.function)
        args = {}
        for param in signature.parameters.values():
            data_type = param.annotation
            if data_type is float:
                args[param.name] = '%%description%%'
            elif data_type is str:
                args[param.name] = '"%%description%%"'
            else:
                raise ValueError(f'Tool does not allow type {str(data_type)}')
        return args

    @property
    def json_string(self) -> str:
        text = f'{{"tool": "{self.name}"'
        for i in self.args:
            text += f', {i}'
        text += '}'
        return text

    def __repr__(self):
        # also describes the tool to the llm
        return f'{self.description} To use, return json in the format {self.json_string}.'


system_prompt = """
YOU MUST FOLLOW THESE INSTRUCTIONS CAREFULLY.                                        
                                                                       
1. To respond to the users message, you can use one of the tools defined below.                                                                               
2. If you decide to use a tool, you must respond in the JSON format.                                                                    
3. To use a tool, just respond with the JSON matching the schema. Nothing else.                                         
4. After you use a tool, the next message you get will contain the result of the tool call.                                                                                
5. REMEMBER: To use a tool, you must respond only in JSON format.                    
6. After you use a tool and receive the result back, respond regularly to answer the users question.                                                                      
7. Only use the tools you are provided.  

Here are the tools you may use:
%%tools%%

Remember, you must answer ONLY with valid json, and nothing else.
"""

prompt = """What is the price of NVIDIA stock right now?"""


def stock_price(stock_name: str) -> str:
    """
    A tool to return the current stock price of a given stock.

    stock_name: The name of the stock you want the price of.
    """
    return 'The time in the UK is 19:38pm'


def current_time(timezone: str) -> str:
    """
    A tool to return the current time in a timezone

    timezone: The timezone you the time from.
    """
    return 'The time is 9:58am'


def test_function_call():
    stock_tool = Tool(stock_price)
    time_tool = Tool(current_time)
    desc = '\n'.join([str(stock_tool), str(time_tool)])
    sys_prompt = system_prompt.replace('%%tools%%', desc)
    result = ollama.generate(model='mistral:7b-instruct-v0.2-q8_0',
                             format='json',
                             system=sys_prompt,
                             prompt=prompt)
    print(result)


if __name__ == '__main__':
    #test_function_call()
    print(str(Tool(stock_price)))
