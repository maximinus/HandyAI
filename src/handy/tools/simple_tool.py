import inspect

from typing import Callable, Any

# a tool will need to communicate via json. So we need to define the json structure somehow


class Tool:
    def __init__(self, func: Callable):
        self.description = func.__doc__
        self.function = func
        self.name = func.__name__
        self.json_string = self.get_func_as_json()

    def get_func_as_json(self):
        signature = inspect.signature(self.function)
        args = [f'"tool": "{self.name}"']
        for param in signature.parameters.values():
            # we only allow numbers and strings
            data_type = param.annotation
            if data_type is float:
                args.append(f'"{param.name}": SOME_NUMBER')
            elif data_type is str:
                args.append(f'"{param.name}": "SOME_TEXT"')
            else:
                raise ValueError(f'Tool does not allow type {str(data_type)}')
        json_args = ', '.join(args)
        return f"{{{json_args}}}"

    def __repr__(self):
        # also describes the tool to the llm
        return f'{self.description}. To use the tool, return json like {self.json_string}.'
