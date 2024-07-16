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


So the basic process of using an LLM is that of a block box:

    Text In -> LLM - > Text Out

To produce a chat, we need to feed the text we put in back into the LLM, along with extra text

    Previous input + previous output -> LLM -> Text Out


TODO: Reduce the complexity of the message objects we have now


Chat
----

Set up a chat instance with a local LLM, and include:

* Keep a memory of previous chats
* Store exchanges in a database of some kind
* Refer to a RAG database to extract information

There are 3 ways to store previous messages:

1: Keep a record of each message, and pass that over to the LLM when recalled
2: Put each question and answer into a RAG database, and when a question is asked, retrieve matches
3: Ask an LLM to pull put the important data and store that data in a database or RAG system

TODO: There has to be a way of knowing the type of things we are talking about, so we can direct the LLM.


Agent
-----

Give an LLM a task to perform

There are different sorts of agents:

* Reactive agents are given some information and then react to it; they hold no state
* Deliberative agents hold some state about the world and react to it in some way
* Social agents hold some state and know about other agents

Agents in general need to be able to access other sources of information, and may need a prompt that details what kind of thing they do

So they need:

* A description (in text)
* The problem (in text)
* A list of functions


Function
--------

A function is something the LLM can do. An LLM can be given a suite of functions to use, and when they are used the LLM is given more information.

If you allow an LLM to use a search engine and ask about todays weather in your location, it may first call the function, then use the result of that information to inform it in it's answer.

A function can also be another LLM


Task
----

A task is a job that needs doing.
It has 2 parts, of which the second is optional. The first part is the actual task itself. The second part is a method to define if the task has been done.

For example, we could define the task and the test like:

* Return the square root of the number 9
* The answer when multiplied by itself should be 9

The test is optional, and may be able to be inferred from the task itself.
