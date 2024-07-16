Handy AI
========

Handy AI is a library designed to make using an LLM locally as easy as possible.


Overview
--------

As a programmer, we can think of LLM systems as very simple: it is just text.
For example

* When we ask an LLM a question, we send text and get back text
* When an agent talks to other agents, they store text
* When we store information about the world, we simply store strings
* When we ask an agent to do function calling, it uses json, but the answers are always strings


Chat
----

Set up a chat instance with a local LLM, and include:

* Keep a memory of previous chats
* Store exchanges in a database of some kind
* Refer to a RAG database to extract information


Agent
-----

Give an LLM a task to perform

There are different sorts of agents:

* Reactive agents are given some information and then react to it; they hold no state
* Deliberative agents hold some state about the world and react to it in some way
* Social agents hold some state and know about other agents


Function
--------

A function is something the LLM can do. An LLM can be given a suite of functions to use, and when they are used the LLM is given more information.

If you allow an LLM to use a search engine and ask about todays weather in your location, it may first call the function, then use the result of that information to inform it in it's answer.


Task
----

A task is a job that needs doing.
It has 2 definitions. The first is the actual task itself. The second definition is a method to define if the task has been done.

For example, we could define the task and the test like:

* Return the square root of the number 9
* The answer when multiplied by itself should be 9

The test is optional, and may be able to be inferred from the task itself.
