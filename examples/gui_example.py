import gradio as gr

from handy.llm.base import Exchange
from handy.llm.ollama_llm import Ollama


def chat_response(message, history):
    model = Ollama(model_name='mistral:latest')
    # each history entry is a list of [user_input, llm_response]
    chats = [Exchange.from_text(x[0], x[1]) for x in history]
    answer = model.message_with_history_streaming(message, chats)
    full_reply = []
    for chunk in answer:
        full_reply.append(chunk)
        yield ''.join(full_reply)


gr.ChatInterface(chat_response).launch()
