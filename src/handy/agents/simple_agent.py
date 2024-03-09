from handy.llm.base import BaseLLM

# An agent is an llm wrapped up with some extra data
# They act like all transformers: they input text and then and output text.
# the llm will have some memory, and also we usually add some leader text,
# which is the description of the role of the agent


class Agent:
    def __init__(self, llm: BaseLLM, role: str, description: str = '', workers: list | None = None):
        self.llm = llm
        self.role = role
        self.description = description
        if workers is None:
            workers = []
        self.workers = workers

    def solve_task(self, task) -> str:
        # given a task, solve it
        # we need to create the prompt.
        task_prompt = f'You are a {self.role}. {task.description}.'
        response = self.llm.message_with_history(task_prompt)
        return response.text
