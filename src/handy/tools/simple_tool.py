import json
import inspect

from typing import Callable, Any

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


class Tool:
    def __init__(self, func: Callable):
        self.name = func.__name__
        self.description = func.__doc__.strip()
        self.function = func
        self.json_string = self.get_func_as_json()

    def get_func_as_json(self):
        signature = inspect.signature(self.function)
        json_data = {'type': 'function'}
        func_data = {'name': self.name, 'description': self.description}
        func_args = {}
        for param in signature.parameters.values():
            # we only allow numbers and strings
            data_type = param.annotation
            if data_type is float:
                func_args[param.name] = 'number'
            elif data_type is int:
                func_args[param.name] = 'integer'
            elif data_type is str:
                func_args[param.name] = 'string'
            elif data_type is bool:
                func_args[param.name] = 'boolean'
            elif data_type is list:
                func_args[param.name] = 'array'
            else:
                raise ValueError(f'Tool does not allow type {str(data_type)}')
        func_data['parameters'] = {'type': 'object', 'properties': func_args}
        json_data['function'] = func_data
        return json.dumps(json_data, indent=4)
