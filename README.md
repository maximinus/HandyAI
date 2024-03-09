# Handy

A python library to make interactions with llms (large language models) simple.

The goal is not only to make it easy to work with llms, but to make the logic around them simple, understandable and easy to write code with.

The library is opinionated and tries to give one (good) way to solve things; "There should be one-- and preferably only one --obvious way to do it."

We believe in simple English to help everybody and we try to name things logically and simply.


## Basic Overview

An llm can be seen as a simple box: we put in text, and we get out text.

However, we can do some very clever things with just this simple box.

We can put in previous messages, so the llm has a history to work with: this gives us chat.
We can add in documentation before our message, so the llm has more data to work with: this gives the llm the ability to talk about data.
We can check the users message and see if we have similar sorts of phrases in a database: this is a RAG system.
We can create 2 or more llms and get them to talk to each other: this is a multi-agent system.
We can tell an llm that a message in a special format will perform some action: this gives us tasks.

We should be able to reason about all of this easily; the cognitive load should be fairly light and thus the code should also be simple.
*The majority of the work we do is based on language and data, thus we should use language and data in our definitions, not code*

We should be able to perform all of these functions locally or non-locally, and we should be able to choose the model we like.


Currently, Handy is in a very early development stage.


## Examples

Single line of chat with Ollama

```
from handy.llm import Ollama

llm = Ollama('mistral:7b-instruct-v0.2-q8_0')
response = llm.message('How big is the moon?')
print(response.text)
```

Simple chat with history

```
from handy.llm import Ollama

llm = Ollama(OLLAMA_MODEL)
while True:
    request = input('Enter your message: ')
    if request == 'exit':
        return
    response = llm.message_with_history(request)
    print(f'LLM: {response.text}')
```
