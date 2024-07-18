from handy.llm import Ollama
from handy.tools import Tool


# define a call we will use
def get_city_temperature(city: str):
    """
    Get the current temperature of a city

    :param city: The name of the city
    :return: The temperature of the city
    """
    return 20


llm = Ollama(model_name='mistral:latest')
tool = Tool(get_city_temperature)
response = llm.solve('Can you tell me the temperature in London right now?', [tool])
print(response.response)
