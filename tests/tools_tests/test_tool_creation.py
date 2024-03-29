import unittest

from handy_ide.tools.simple_tool import Tool

# example functions
def no_args():
    # no args, should work fine
    pass


def float_arg(foo: float):
    pass


def str_arg(foo: str):
    pass


def int_arg(foo: int):
    # not allowed
    pass


def list_arg(foo: list):
    # not allowed
    pass


def simple_test(foo: str):
    """Hello!"""
    pass


class TestSimpleTool(unittest.TestCase):
    # if there is no test, we are just checking there is no exception raised
    def test_no_args(self):
        Tool(no_args)

    def test_float(self):
        Tool(float_arg)

    def test_str(self):
        Tool(str_arg)

    def test_int(self):
        # note that self.assertRaises has issues with exception in __init__ functions
        try:
            Tool(int_arg)
        except ValueError:
            return
        raise AssertionError('Did not raise exception')

    def test_list(self):
        try:
            Tool(list_arg)
        except ValueError:
            return
        raise AssertionError('Did not raise exception')

    def test_simple(self):
        my_tool = Tool(simple_test)
        tool_text = str(my_tool)
        self.assertTrue('Hello' in tool_text)
        self.assertTrue('foo' in tool_text)
