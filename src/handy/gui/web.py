import gradio as gr

from handy.llm.base import BaseLLM


def gradio_response(llm_model: BaseLLM):
    # store the llm as a closure, and return the inner function
    llm = llm_model

    def responder(message, history):
        nonlocal llm
        # we actually don't need the history as we store it ourselves
        response = llm_model.chat(message)
        all_chunks = []
        for chunk in response:
            all_chunks.append(chunk)
            yield ''.join(all_chunks)

    return responder


def web_chat(llm_model):
    llm_function = gradio_response(llm_model)
    gr.ChatInterface(llm_function).launch()
