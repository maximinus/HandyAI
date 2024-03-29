from handy_ide.llm.ollama_llm import Ollama
from handy_ide.agents.simple_agent import Agent
from handy_ide.tasks.simple_task import Task


# first we need an llm
llm = Ollama('mistral:7b-instruct-v0.2-q8_0')
# an agent to actually do the task
agent = Agent(llm, role='Chef')
# a task to perform
task = Task(description='Please write a recipe for eggs benedict')

print(agent.solve_task(task))
