# Handy.AI

Handy.AI is a library of tools for working with a local LLM.

The basic building block when using Handy is a string. You can imagine an LLM in the following way: you pass it a string, and it returns a string.

For example, if we input "What is the biggest whale?" we might get "The Blue Whale".

Handy.AI contains these separate parts:

1: An interface to talk to an LLM
2: An easy way to store conversations with an LLM
3: Agents, which are simple LLMs with a task or goal
4: Tools, which are things an LLM can use to help solve a task
5: Data stores, which hold information which an LLM can be fed information from.

Since functions and agents simply accept text and reply with text, an agent can be used as a kind of tool; we can give an agent a task and a list of agents and tools it could use to solve the task.


## Goals

The aim of Handy.AI is simple:

**To give a user the tools to ensure that an AI has all the resources it needs to solve a given problem.**

To ensure this, we must give the AI the ability to make decisions about what is important, *which may include the agent writing it's own tools or agents*.




## Techstack

Handy is written in Python, using the Ollama API to access LLM models.
LanceDB is used as the RAG backend.
