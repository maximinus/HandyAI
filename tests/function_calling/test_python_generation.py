import ast
import ollama

from handy_ide.tools.run_python import runner

# the aim here is to have an llm provide Python code
# We do this in the following way
# Unlike having a tool, we simply ask the llm to provide python code only
# We then run the code, and obtain any error messages, which are then passed back into the conversation
# We do this until the code is correct, or after a number of iterations


system_prompt = """
You are a senior Python programmer. You produce well written, commented, standard working Python code.
Your response to this request MUST be ONLY valid Python code, do not any explanations of the code except in comments.
""".strip()

request = """
Create a python function accepts 2 arguments, each of which is a list that represents the co-ords of a point on the plane.
The function will return the distance between 2 points on a plane.
""".strip()

request_test = """
Here is a python function that will return the distance between 2 points on a plane.

```
%%code%%
```

Please return an example of calling the function with valid arguments in python.
You must ONLY include the python code to create any arguments and call the function.
""".strip()

example_code = '''
python
import math

def distance_between_points(point1, point2):
    """
    Calculates the Euclidean distance between two points represented as lists of x and y coordinates.

    :param point1: List of two elements, x and y coordinates of the first point.
    :param point2: List of two elements, x and y coordinates of the second point.
    :return: The Euclidean distance between the two points.
    """

    x1, y1 = point1
    x2, y2 = point2

    # Calculate the difference between coordinates
    dx = x2 - x1
    dy = y2 - y1

    # Use the Pythagorean theorem to calculate the distance
    return math.sqrt(dx ** 2 + dy ** 2)
'''.strip()

example_test = """
point1 = [1, 2]
point2 = [4, 6]
distance = distance_between_points(point1, point2)
print(distance)
""".strip()


class ParseError(Exception):
    pass


class PythonFunc:
    def __init__(self, name, args):
        self.name = name
        self.args = args

    def __repr__(self):
        arg_text = ', '.join(self.args)
        return f'{self.name}({arg_text})'


def get_functions_from_code(code: str):
    # we have some Python code in the form of a string
    # we want to wander through this and we should (!) find a python function
    # return the names of the python function that we found
    try:
        tree = ast.parse(code, feature_version=(3, 9))
    except ValueError as ex:
        raise ParseError
    functions = []
    for node in ast.walk(tree):
        if isinstance(node, ast.FunctionDef):
            function_name = node.name
            args = [arg.arg for arg in node.args.args]
            functions.append(PythonFunc(function_name, args))
    return functions


def get_python_code():
    result = ollama.generate(model='mistral:7b-instruct-v0.2-q8_0',
                             system=system_prompt,
                             prompt=request)
    return result['response']


def get_example(code):
    example_prompt = request_test.replace('%%code%%', code)
    result = ollama.generate(model='mistral:7b-instruct-v0.2-q8_0',
                             system=system_prompt,
                             prompt=example_prompt)
    return result['response']


def strip_python_header(code: str) -> str:
    # sometimes the example code starts with the word "python"; if it does, just strip that out
    if code.startswith('python'):
        code = '\n'.join(code.split('\n')[1:])
    if code.startswith('```'):
        # remove first and last line
        code = '\n'.join(code.split('\n')[1:-1])
    return code


def add_code_and_example(code, example):
    example_lines = example.split('\n')
    example_lines = [f'    {x}' for x in example_lines]
    example_lines.insert(0, "if __name__ == '__main__':")
    example_lines.append('')
    return code + '\n\n' + '\n'.join(example_lines)


def get_tested_code():
    #code = get_python_code()
    code = example_code
    if len(code) == 0:
        print('No code sent!')
        return
    code = strip_python_header(code)
    funcs = get_functions_from_code(code)
    if len(funcs) != 1:
        print('Got more than one function!')
        return
    # now we have the full code. Ask the llm to produce an example of calling the code
    #test_code = get_example(code)
    test_code = example_test
    example = strip_python_header(test_code)
    test_code = add_code_and_example(code, example)
    result = runner.run_python(test_code)
    print(result.output)


if __name__ == '__main__':
    get_tested_code()
