from handy.llm import Ollama

llm = Ollama(model_name='mistral:latest')

prompt = """
[AVAILABLE_TOOLS] [{"type": "function", "function": {"name": "get_current_weather", "description": "Get the current weather", "parameters": {"type": "object", "properties": {"location": {"type": "string", "description": "The city and state, e.g. San Francisco, CA"}, "format": {"type": "string", "enum": ["celsius", "fahrenheit"], "description": "The temperature unit to use. Infer this from the users location."}}, "required": ["location", "format"]}}}][/AVAILABLE_TOOLS][INST] What is the weather like today in San Francisco [/INST]
"""

response = llm.solve(prompt, [])
print(response.response)
