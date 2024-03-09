from handy.llm.ollama_llm import Ollama

# simple example of sending the llm a single request and printing the response
# you may change the model if you like

llm = Ollama('mistral:7b-instruct-v0.2-q8_0')
response = llm.message('How big is the moon?')
print(response.get_text_response())
