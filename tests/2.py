import requests
import base64
import json

def load_image_base64(image_path):
    with open(image_path, "rb") as f:
        return base64.b64encode(f.read()).decode("utf-8")

def call_ollama_with_image(prompt_text, image_path, model="qwen2.5vl:32b", host="http://192.168.235.62:11434"):
    # 加载图像并编码为 base64
    image_base64 = load_image_base64(image_path)

    # 构造请求体
    payload = {
        "model": model,
        "messages": [
            {
                "role": "user",
                "content": prompt_text,
                "images": [image_base64]
            }
        ],
        "stream": False
    }

    # 发起 POST 请求
    url = f"{host}/v1/chat/completions"
    response = requests.post(url, headers={"Content-Type": "application/json"}, json=payload)

    if response.status_code == 200:
        result = response.json()
        print("✅ Ollama response:\n", result['choices'][0]['message']['content'])
        return result['choices'][0]['message']['content']
    else:
        print(f"❌ Failed: {response.status_code}")
        print(response.text)
        return None

call_ollama_with_image("What is this?", "./442.jpg")