from flask import Flask, request, jsonify
from flask_cors import CORS
import shutil
import tempfile
import os
from pathlib import Path
from openai import OpenAI
import base64
import re

from src.llm_client import prepare_ollama_messages, get_ollama_response, get_openai_response
from src.prompts import SYSTEM_PROMPT
from src.utils import process_image

# Ollama 配置
OLLAMA_MODEL = 'qwen2.5vl:32b'
OLLAMA_HOST = 'http://192.168.235.62:11434'
OLLAMA_KEY = 'KEY'
# OLLAMA_MODEL = 'qwen2.5vl:latest'
# OLLAMA_HOST = 'http://127.0.0.1:11434'

app = Flask(__name__)
CORS(app, supports_credentials=True)

@app.route('/infer', methods=['POST'])
def infer_image():
    # 1. 保存上传的图片到临时文件
    if 'file' not in request.files:
        return jsonify({'error': '未找到文件参数 file'}), 400
    file = request.files['file']
    try:
        suffix = Path(file.filename).suffix or ".png"
        with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as tmp:
            shutil.copyfileobj(file.stream, tmp)
            tmp_path = tmp.name
    except Exception as e:
        return jsonify({'error': f'图片保存失败: {e}'}), 500

    print(f"Saving image to {tmp_path}")
    # 2. 构造 task_history
    task_history = [
        ((tmp_path,), None),
        (SYSTEM_PROMPT, None),
    ]

    # 3. 消息准备与推理
    print(f"Starting prepare the LLM messages......")
    ollama_messages, error = prepare_ollama_messages(task_history, process_image)
    if error:
        os.remove(tmp_path)
        return jsonify({'error': error}), 500

    print(f"Calling LLM for image processing......")
    response, error = get_ollama_response(ollama_messages, OLLAMA_MODEL, OLLAMA_HOST, OLLAMA_KEY)
    os.remove(tmp_path)
    if error:
        return jsonify({'error': error}), 500

    # 4. 只返回 JSON（去除多余内容）
    try:
        import json
        result = json.loads(response)
        return jsonify(result)
    except Exception:
        return jsonify({'raw': response})

@app.route('/infer_openai', methods=['POST'])
def infer_openai():
    if 'file' not in request.files:
        return jsonify({'error': '未找到文件参数 file'}), 400
    file = request.files['file']
    try:
        suffix = Path(file.filename).suffix or ".png"
        with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as tmp:
            shutil.copyfileobj(file.stream, tmp)
            tmp_path = tmp.name
    except Exception as e:
        return jsonify({'error': f'图片保存失败: {e}'}), 500

    # 推理参数
    MODEL = "qwen2.5vl:32b"
    HOST = "http://192.168.235.62:11434"
    KEY = "KEY"
    from src.prompts import SYSTEM_PROMPT

    try:
        response_content, error = get_openai_response(tmp_path, MODEL, HOST, KEY)
        os.remove(tmp_path)
        print(f"====> {response_content}")
        if error:
            return jsonify({'error': error}), 500
        import json, re
        # --- 优化：自动提取严格的 JSON 数组 ---
        cleaned = response_content.strip()
        # 去除 markdown 代码块
        cleaned = re.sub(r'^```[a-zA-Z]*', '', cleaned)
        cleaned = re.sub(r'```$', '', cleaned)
        # 自动定位第一个 [ 和最后一个 ]
        start = cleaned.find('[')
        end = cleaned.rfind(']')
        if start != -1 and end != -1 and end > start:
            json_str = cleaned[start:end+1]
            try:
                result = json.loads(json_str)
                if isinstance(result, list):
                    return jsonify(result)
                else:
                    return jsonify({'error': 'LLM返回内容不是JSON数组', 'raw': response_content}), 500
            except Exception as e:
                return jsonify({'error': f'内容无法解析为JSON数组: {e}', 'raw': response_content}), 500
        else:
            return jsonify({'error': '未找到有效的JSON数组', 'raw': response_content}), 500
    except Exception as e:
        if os.path.exists(tmp_path):
            os.remove(tmp_path)
        return jsonify({'error': str(e)}), 500

# 启动方法（命令行）
# flask --app src.api run --host 0.0.0.0 --port 8000 --reload 