from typing import Callable

# A task is something we would like to do or happen.
# What we mean by *do* is very important.
# An llm by default can only ever convert text to text.
## It's response may be right, or it may be wrong, and the for the interesting cases the latter is usual.
# You can use a tool to determine if something is correct, however a tool must be defined in Python.
# In theory you can let an llm determine if something it correct, however it could always be wrong.
# A task does the usual thing; ultimately it takes in some text, and it returns some text.

# A simple task would just be one agent. It would read in your text and then return some text.
# Then:
#    * Some more text is put in, i.e. a conversation is started
#    * It decides it has finished (which is always after the first response with no tool)
#    * It has some way of testing correctness, in which it may try to fix itself and therefore try many times.

# A more complex example could be 3 or 4 llms.
# For this task you need a manger who has the ability to tell other agents to do the work.


class Task:
    def __init__(self, description: str, completed_check: Callable|None):
        self.description = description
        self.completed_check = completed_check

    def is_completed(self):
        # is this task completed? If no check is given, the answer is always "Yes"
        if self.completed_check is None:
            return True
        return self.completed_check(self)
