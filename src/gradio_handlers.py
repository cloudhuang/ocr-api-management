import gradio as gr
import pprint

from src.utils import parse_text_for_display, process_image
from src.llm_client import prepare_ollama_messages, get_ollama_response


def add_text(history, task_history, text):
    """
    Adds a user's text input to the chat history.
    """
    if not text:
        return history, task_history, ""
    
    history = history or []
    task_history = task_history or []
    
    history.append((parse_text_for_display(text), None))
    task_history.append((text, None))
    
    return history, task_history, ""


def add_file(history, task_history, file):
    """
    Adds a user's file upload to the chat history.
    """
    history = history or []
    task_history = task_history or []
    
    history.append(((file.name,), None))
    task_history.append(((file.name,), None))
    
    return history, task_history


def reset_user_input():
    """
    Clears the user input textbox.
    """
    return gr.update(value="")


def reset_state(task_history):
    """
    Clears the entire chat history.
    """
    if task_history:
        task_history.clear()
    return []


def predict(chatbot, task_history, args):
    """
    The main prediction function. It prepares messages, calls the Ollama API,
    and updates the chatbot UI.
    """
    print("\n" + "=" * 20 + " NEW PREDICT CALL " + "=" * 20)
    print("DEBUG: Current task_history:")
    pprint.pprint(task_history)

    chat_query = chatbot[-1][0]
    query = task_history[-1][0]

    if not query and not (isinstance(query, (tuple, list))):
        chatbot.pop()
        task_history.pop()
        return chatbot

    print(f"User Query: {parse_text_for_display(str(query))}")

    # Prepare messages for Ollama API
    # We pass the process_image function from utils here
    ollama_messages, error = prepare_ollama_messages(task_history, process_image)
    if error:
        chatbot[-1] = (chat_query or "File Upload", error)
        return chatbot

    # Get response from Ollama
    full_response, error = get_ollama_response(
        ollama_messages, args.ollama_model, args.ollama_host
    )
    if error:
        chatbot[-1] = (parse_text_for_display(chat_query), error)
        return chatbot

    # Update chatbot and task history with the response
    chatbot[-1] = (parse_text_for_display(chat_query), parse_text_for_display(full_response))
    task_history[-1] = (query, full_response)

    return chatbot


def regenerate(chatbot, task_history, args):
    """
    Regenerates the last response from the assistant.
    """
    if not task_history:
        return chatbot
    
    item = task_history[-1]
    if item[1] is None:
        return chatbot
    
    # Remove the last answer to regenerate it
    task_history[-1] = (item[0], None)
    
    # Remove the last response from the UI
    chatbot.pop(-1)
    
    # Add a new entry to the UI with a placeholder for the response
    chatbot.append((parse_text_for_display(str(item[0])), None))
    
    # Call predict to get a new response
    return predict(chatbot, task_history, args) 