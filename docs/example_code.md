Handy basic rules
=================

**1: Handy is opinionated**

Handy does not offer a multitude of rag systems, or different ways of doing things.
We stick with one way and do that well to solve the problems we have.

**2: Handy is simple to use**

We want the functionality to be simple, so that it is easy to make what you want

**3: Handy does not over-use abstractions**

What Handy is doing under the hood should be easy to reason, so that it makes using it easier.



Example Code
============

Here we want to show some example code, as otherwise we can go the wrong way quickly.

This is because what we want is a nice front end to the API, and as little complexity as we can.


Simple query
------------

We at least to define an LLM of some kind.

We can do this like:

    from handy.llm import Ollama

    llm = Ollama('mistral:latest')


Now we want to submit a query:

    llm.query('How cold is the north pole?')

This will return text, also the llm will hold some info about the last interaction.

    llm.query('How cold is the north pole?', chunked=True)

This returns an iterator over the various chunks:

    for chunk in llm.query('How cold is the north pole?', chunked=True):
        print(chunk)


Perhaps we want to chat, in which case:

    llm.chat('How cold is the north pole')

Also returns text, however the next time chat is called, it will pass to the llm the current chat history.

This can be cleared:

    llm.clear_chat()


When we want to remember
------------------------

This time, we need to tell the llm to remember the chat:

    llm.use_store(name=None)

This returns the name of a store we can use to hold the chat data. This is a local sqlite database.
The function returns the name of the store: either one we specified, or a random one if we did not specify.

The database will store the text results, and the timestamp of the last interaction.

To restore a chat to a former status, you need to use the name, or just use the last one in the database:

    llm.recall(name=None)

Of course, you might just want to continue an old chat and update:

    llm.recall_and_use(name=None)


GUI front end
-------------

We want to be able to see all of these things in a GUI.

    from handy.gui import web_chat

    web_chat(llm)

Will bring up a GUI to enable chat. Of course, you can recall an old chat:

    from handy.llm import Ollama
    from handy.gui import web_chat

    llm.recall_and_use(name)
    web_chat(llm)


RAG systems
-----------

We want to store things in a RAG. For this, we need an embedding, which is based on a model.

    llm.get_embedding()

We also need a store name (for the vector db):

    from handy.rag import store, retrieve

    store(name, embedding, text)

To get data back:

    retreive(name, embedding, total_matches=1)

We also might need to get the distance between 2 vectors easily:

    from handy.rag import distance

    distance(text1, text2, embedding)

Given a rag system, we may want to pull information out of it based on the prompt:

    llm.use_rag(store)
    llm.ignore_rag()


Capturing Data
--------------

Often you want to populate a store with some data beforehand.

    from handy.rag import parse_data

    parse_data(store, data)

This is tricky and requires some work.


Agents
------

Agents are simply defined

    from handy.agent import Agent

    my_agent = Agent(title, description, functions)

Other agents act as functions. So an agent can be given other agents.
Agents don't do anything until given a task.


Functions
---------

A function is simple: it is something an agent can use to get an answer.
Like most things, it is simple, text in and text out to a degree, although functions are defined using JSON.

An agent can be used as a function, the function call would be to ask the agent to do something.

    from handy.agent import Agent
    from handy.functions import search

    programmer = Agent('Programmer', 'You are a master Python programmer', [search])
    manager = Agent(Manager, 'You manage Python programmers', [programmer])

    task = Task('Program a snake game')

    manager.solve_task(task)


Tasks
-----

Tasks are a simple text definition of some job.
They may also come with a definition of success:

1: A python function that calculates success
2: A text description of success
