from handy.gui import web_chat
from handy.llm.ollama_llm import Ollama

# create an llm and then fire up the gradio front end with it

llm = Ollama('mistral:latest')
web_chat(llm)
