import unittest

from handy.tools import Tool
from handy.llm.ollama_llm import check_tool_response


# here is the real response of an LLM and a function for it
RESPONSE = '[TOOL_CALLS] [{"name": "get_city_temperature", "arguments": {"city": "London"}}]'


def get_city_temperature(city: str):
    """
    Get the current temperature of a city

    :param city: The name of the city
    :return: The temperature of the city
    """
    raise AttributeError


class TestFunctionCalled(unittest.TestCase):
    def test_function_called(self):
        tool = Tool(get_city_temperature)
        with self.assertRaises(AttributeError):
            check_tool_response(RESPONSE, [tool])
