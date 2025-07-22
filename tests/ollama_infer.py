import os
import sys
from pathlib import Path

from src.llm_client import prepare_ollama_messages, get_ollama_response
from src.prompts import USER_PROMPT
from src.utils import process_image

# 允许直接命令行运行本脚本时找到 src 目录
sys.path.append(str(Path(__file__).parent.parent / 'src'))

# ==== 配置区 ====
OLLAMA_MODEL = 'qwen2.5vl:3b'  # 或你的多模态模型名
OLLAMA_HOST = 'http://localhost:11434'  # Ollama 服务地址
OLLAMA_KEY = 'KEY'

# 测试图片和文本
TEST_IMAGE_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), '442.jpg'))
TEST_TEXT = USER_PROMPT

# ==== 构造 task_history，模拟一次多模态对话 ====
task_history = [
    ((TEST_IMAGE_PATH,), None),  # 上传图片
    (TEST_TEXT, None),  # 紧跟一条文本
]

# ==== 构造消息体 ====
ollama_messages, error = prepare_ollama_messages(task_history, process_image)
if error:
    print(f"[ERROR] {error}")
    sys.exit(1)

# ==== 推理调用 ====
response, error = get_ollama_response(ollama_messages, OLLAMA_MODEL, OLLAMA_HOST, OLLAMA_KEY)
if error:
    print(f"[ERROR] {error}")
else:
    print("\n=== Ollama 推理结果 ===")
    print(response)
