from handy.llm import BaseLLM

# An agent is an llm wrapped up with some extra data
# They act like all transformers: they input text and then and output text.
# the llm will have some memory, and also we usually add some leader text,
# which is the description of the role of the agent


class Agent:
    def __init__(self, llm: BaseLLM, name: str, description: str, workers: list|None):
        self.llm = llm
        self.name = name
        self.description = description
        if workers is None:
            workers = []
        self.workers = workers
