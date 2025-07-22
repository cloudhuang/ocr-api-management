import os
import sys
from pathlib import Path

from src.llm_client import prepare_ollama_messages, get_ollama_response, get_openai_response
from src.prompts import USER_PROMPT
from src.utils import process_image

# 允许直接命令行运行本脚本时找到 src 目录
sys.path.append(str(Path(__file__).parent.parent / 'src'))

# 测试图片和文本
TEST_IMAGE_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), 'claims.png'))
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

PROMPT = """
你是一個高精度的 AI 表單辨識服務。你的唯一任務是分析在此次請求中提供的圖片，並根據下方的{{輸出格式}}要求，返回识别的结果。**

**核心指令：**
分析提供的圖片，识别书图片中的内容。你的所有輸出都必須基於圖片中的視覺證據。

---
**辨識準確性與置信度規則 (Accuracy and Confidence Rules)：**
1.  **高置信度原則**：只有在您對辨識結果有高置信度時，才輸出文字內容。
2.  **完整识别图片内容**: 图片是一张INVOICE的发票，包括发票抬头、发票号、日期、金额等信息。请确保识别出所有相关信息。

**輸出格式：絕對嚴格**
- 你的回覆**必須是、也只能是**一個完整的Markdown的文本。
- 图片识别的文本内容，通过markdown的语法返回
- 如果识别出来的是文本，你需要严格遵行文本的格式。
- 如果识别出来的是表格，你需要严格遵行原表格的格式。
- 如果识别出来的表格内容，直接返回markdown格式的表格,格式参考{{Markdown表格参考}}
- 严格遵循Markdown语法，确保格式正确。
- 使用英文回复

## Markdown表格参考
| Month | Savings |
| -------- | ------- |
| January | $250 |
| February | $80 |
| March | $420 |


"""
# ==== 推理调用 ====
response, error = get_openai_response(image_path=TEST_IMAGE_PATH, model='qwen2.5vl:32b', host='http://192.168.235.62:11434', key="KEY", prompt=PROMPT)
if error:
    print(f"[ERROR] {error}")
else:
    print("\n=== 推理结果 ===")
    print(response)
