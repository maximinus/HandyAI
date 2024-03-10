import inspect
from typing import Any


def my_tool(search_text: str, value: float) -> str:
    """Used as a test example"""
    return f"{search_text}, {value}"


# convert that to a json format
# we don't care about the return type at all
def function_signature_to_json(func):
    signature = inspect.signature(func)
    args = [f'"tool": {func.__name__}']
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


foo = function_signature_to_json(my_tool)
print(foo)
