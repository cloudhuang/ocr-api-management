import base64
import requests

from src.prompts import SYSTEM_PROMPT

image_path = "./442.jpg"
with open(image_path, "rb") as f:
    encoded = base64.b64encode(f.read()).decode("utf-8")

# 注意图像格式要写成 image/jpeg 或 image/png
img_tag = f'<img src="data:image/jpeg;base64,{encoded}"/>'

# 拼接完整 prompt
prompt = SYSTEM_PROMPT + img_tag + "\n请识别图中的手写部分的文字内容，并返回符合要求的JSON数据"

# 向 Ollama 发送请求
response = requests.post(
    "http://192.168.235.62:11434/v1/chat/completions",
    json={
        "model": "qwen2.5vl:32b",
        "messages": [
            {"role": "user", "content": prompt}
        ],
        "stream": False
    }
)

result = response.json()
print(result["choices"][0]["message"]["content"])