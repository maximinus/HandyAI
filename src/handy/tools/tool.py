import json
import inspect

from typing import Callable

from handy.exceptions import ToolNoDocString, ToolDescriptionError, ToolMissingParamDescription, ToolCallMissingParam

# a tool will need to communicate via json.
# An example of the JSON format is as follows:

"""
{
    'type': 'function',
    'function': {
        'name': 'get_flight_times',
        'description': 'Get the flight times between two cities',
        'parameters': {
            'type': 'object',
            'properties': {
                'departure': {
                    'type': 'string',
                    'description': 'The departure city (airport code)',
                },
                'arrival': {
                    'type': 'string',
                    'description': 'The arrival city (airport code)',
                },
            },
            'required': ['departure', 'arrival'],
          },
        },
      }
}

Of course the parameters are always a single object

"""


def get_function_description(docstring):
    description = []
    for line in docstring.split('\n'):
        line = line.strip()
        if line.startswith(':param'):
            break
        if len(line) > 0:
            description.append(line)
    return ' '.join(description)


def get_param_descriptions(docstring):
    params = {}
    # go line by line
    for line in docstring.split('\n'):
        line = line.strip()
        if line.startswith(':param'):
            # strip to the second ':
            parts = line.split(':')
            if len(parts) < 3:
                raise ToolDescriptionError('Malformed docstring for tool')
            description = ':'.join(parts[2:])
            # the first part should start with 'param '
            if not parts[1].startswith('param '):
                raise ToolDescriptionError('Param description error in docstring')
            var_name = parts[1][6:]
            params[var_name] = description
    return params


class Tool:
    def __init__(self, func: Callable):
        self.name = func.__name__
        self.func = func
        if func.__doc__ is None:
            raise ToolNoDocString(f'{func} must contain a valid docstring in reST format')
        self.description = get_function_description(func.__doc__)
        self.json_string = self.get_func_as_json()

    def call_function(self, call_data):
        signature = inspect.signature(self.func)
        args = []
        for param in signature.parameters.values():
            if param.name not in call_data:
                raise ToolCallMissingParam(f'Missing {param.name}')
            args.append(call_data[param.name])
        # TODO: Check the call actually worked
        return call_data(*args)

    def get_func_as_json(self):
        signature = inspect.signature(self.func)
        json_data = {'type': 'function'}
        func_data = {'name': self.name, 'description': self.description}
        func_args = {}
        # obtain the params list from the docstring
        param_descriptions = get_param_descriptions(self.func.__doc__)
        for param in signature.parameters.values():
            if param.name not in param_descriptions:
                raise ToolMissingParamDescription(f'No description for parameter {param.name}')
            # we only allow numbers and strings
            data_type = param.annotation
            if data_type is float:
                f_type = 'number'
            elif data_type is int:
                f_type = 'integer'
            elif data_type is str:
                f_type = 'string'
            elif data_type is bool:
                f_type = 'boolean'
            elif data_type is list:
                f_type = 'array'
            else:
                raise ValueError(f'Tool does not allow type {str(data_type)}')
            func_args[param.name] = {'type': f_type, 'description': param_descriptions[param.name]}
        required = [x.name for x in signature.parameters.values()]
        func_data['parameters'] = {'type': 'object', 'properties': func_args, 'required': required}
        json_data['function'] = func_data
        return json.dumps(json_data)
