import os

import ollama
from openai import OpenAI
import copy
import pprint
import base64

from src.prompts import USER_PROMPT
from src.utils import is_video_file, process_image


def prepare_ollama_messages(task_history, process_image_func):
    """
    Prepares the message history in the format required by the Ollama API.
    It processes images and structures the conversation history.
    """
    ollama_messages = []
    history_to_process = copy.deepcopy(task_history)
    i = 0
    while i < len(history_to_process):
        q, a = history_to_process[i]
        user_msg = {'role': 'user', 'content': '', 'images': []}

        if isinstance(q, (tuple, list)):
            image_path = q[0]
            if is_video_file(image_path):
                # Return an error message if a video file is detected
                return None, "OLLAMA does not support video files. Please upload an image."

            # Process the image using the provided function
            processed_image_path = process_image_func(image_path)
            with open(processed_image_path, "rb") as f:
                user_msg['images'].append(f.read())

            # Check if the next message is a text prompt for the image
            if (i + 1) < len(history_to_process):
                next_q, next_a = history_to_process[i + 1]
                if next_a is None and not isinstance(next_q, (tuple, list)):
                    user_msg['content'] = next_q
                    i += 1  # Skip the next item as it's been consumed
        else:
            user_msg['content'] = q

        ollama_messages.append(user_msg)

        if a is not None:
            ollama_messages.append({'role': 'assistant', 'content': a})

        i += 1
    return ollama_messages, None


def get_ollama_response(messages, model, host, key):
    """
    Sends a request to the Ollama API and returns the response.
    """
    # --- DEBUG: Log the message payload being sent to Ollama ---
    print("\nDEBUG: Messages being sent to Ollama API:")
    debug_messages = copy.deepcopy(messages)
    for msg in debug_messages:
        if msg.get('images'):
            msg['images'] = [f"<image bytes, len={len(img)}>" for img in msg['images']]
    pprint.pprint(debug_messages)
    print("-" * 50)

    try:
        client = ollama.Client(host=host)
        response = client.chat(
            model=model,
            messages=messages,
            stream=False  # Blocking call
        )

        # --- DEBUG: Print the entire raw response from Ollama ---
        print("\nDEBUG: Raw response object from Ollama:")
        pprint.pprint(response)
        print("-" * 50)

        full_response = response['message']['content']
        print(f"Ollama ({model}): {full_response}")
        return full_response, None

    except Exception as e:
        print(f"An error occurred with OLLAMA: {e}")
        error_message = (
            f"**Error:** Could not connect to OLLAMA or process the request. "
            f"Please ensure OLLAMA is running and the model '{model}' is available.\n\n"
            f"*Details: {e}*"
        )
        return None, error_message 


def get_openai_response(image_path, model, host, key):
    """
    用 OpenAI SDK 方式调用多模态模型，支持图片+文本推理。
    先自动锐化图片，再推理。
    返回 (response_content, error)
    """
    try:
        processed_image_path = process_image(image_path)
        with open(processed_image_path, "rb") as image_file:
            base64_image = base64.b64encode(image_file.read()).decode('utf-8')
        client = OpenAI(
            api_key=key,
            base_url=host.rstrip("/") + "/v1",
        )
        response = client.chat.completions.create(
            model=model,
            messages=[
                {
                  "role": "user",
                  "content": [
                    {
                      "type": "text",
                      "text": USER_PROMPT
                    },
                    {
                      "type": "image_url",
                      "image_url": {
                        "url": f"data:image/jpeg;base64,{base64_image}"
                      }
                    }
                  ]
                }
              ],
              stream=False,
              stream_options={"include_usage":True}
            )
        content = response.choices[0].message.content
        print(f"[DEBUG] = OpenAI({model}): {content}")
        return content, None
    except Exception as e:
        print(f"An error occurred with OpenAI SDK: {e}")
        error_message = (
            f"**Error:** Could not connect to OpenAI SDK or process the request. "
            f"Please ensure the OpenAI-compatible server is running and the model '{model}' is available.\n\n"
            f"*Details: {e}*"
        )
        return None, error_message 