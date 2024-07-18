import json
import unittest

from handy.tools import Tool
from handy.exceptions import ToolNoDocString


# here is an example function we want to turn into a tool

def get_weather1(location: str):
    return f'The weather in {location}is cool and breezy, a mild 20C'


def get_weather2(location: str):
    """
    Call to get the current weather in a location

    :param location: The city or place
    """
    return f'The weather in {location}is cool and breezy, a mild 20C'


class TestToolJson(unittest.TestCase):
    def test_fails_no_docstring_function(self):
        with self.assertRaises(ToolNoDocString):
            Tool(get_weather1)

    def test_passes_with_docstring(self):
        Tool(get_weather2)

    def test_extracts_function_name(self):
        tool = Tool(get_weather2)
        data = json.loads(tool.json_string)
        self.assertTrue('function' in data)

    def test_name_is_correct(self):
        tool = Tool(get_weather2)
        data = json.loads(tool.json_string)
        self.assertEqual(data['function']['name'], 'get_weather2')
