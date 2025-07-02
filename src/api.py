import os
import shutil
import tempfile
from pathlib import Path

from flasgger import Swagger, swag_from  # Import Flasgger
from flask import Flask, request, jsonify
from flask_cors import CORS

from src.llm_client import get_openai_response

# Ollama 配置
OLLAMA_MODEL = 'qwen2.5vl:32b'
OLLAMA_HOST = 'http://192.168.235.62:11434'
OLLAMA_KEY = 'KEY'
# OLLAMA_MODEL = 'qwen2.5vl:latest'
# OLLAMA_HOST = 'http://127.0.0.1:11434'

app = Flask(__name__)
CORS(app, supports_credentials=True)


# Initialize Swagger inside app context
swagger = Swagger(app)


@app.route('/infer', methods=['POST'])
@swag_from({
    'summary': 'Process an image file using OpenAI compatible API',
    'description': 'Uploads an image file and processes it using the configured LLM service',
    'parameters': [
        {
            'name': 'file',
            'in': 'formData',
            'type': 'file',
            'required': True,
            'description': 'The image file to be processed'
        }
    ],
    'responses': {
        '200': {
            'description': 'Successful response with processed result',
            'schema': {
                'type': 'object',
                'properties': {
                    'result': {'type': 'string', 'description': 'Processed result from LLM'}
                }
            }
        },
        '400': {
            'description': 'Bad request, no file uploaded',
            'schema': {'type': 'object', 'properties': {'error': {'type': 'string'}}}
        },
        '500': {
            'description': 'Internal server error',
            'schema': {'type': 'object', 'properties': {'error': {'type': 'string'}}}
        }
    }
})
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

    try:
        response_content, error = get_openai_response(tmp_path, MODEL, HOST, KEY)
        os.remove(tmp_path)
        print(f"【DEBUG】====> {response_content}")
        if error:
            return jsonify({'error': error}), 500
        import json, re

        cleaned = response_content.strip()
        # 去除 markdown 代码块
        cleaned = re.sub(r'^```[a-zA-Z]*', '', cleaned)
        cleaned = re.sub(r'```$', '', cleaned)

        import json
        result = json.loads(cleaned)
        return jsonify(result)
    except Exception as e:
        if os.path.exists(tmp_path):
            os.remove(tmp_path)
        return jsonify({'error': str(e)}), 500

# 启动方法（命令行）
# flask --app src.api run --host 0.0.0.0 --port 8000 --reload
