import json
from typing import Callable, Any

# a tool will need to communicate via json. So we need to define the json structure somehow


class Tool:
    def __init__(self, description: str = '', function: Callable[[Any], str]|None = None, input_format: str = ''):
        self.description = description
        self.function = function
        self.input_format = input_format

    def describe(self) -> str:
        # TODO: describes the tool to the llm
        return ''

    def run(self, json_data: str) -> str:
        if self.function is None:
            return ''
        try:
            function_arguments = json.loads(json_data)
        except json.decoder.JSONDecodeError as ex:
            # TODO: Something went wrong. Clarify for the sender
            return f'JSON error on input json: {ex}'
        return self.function(function_arguments)
