import os
import shutil
import tempfile
from pathlib import Path

from flasgger import swag_from
from flask import Blueprint, request, jsonify

from src.config import VLLM_MODEL, OLLAMA_KEY, OLLAMA_HOST
from src.llm_client import get_openai_response

# Create a blueprint for the infer API
infer_api = Blueprint('infer_api', __name__)


@infer_api.route('/infer', methods=['POST'])
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

    try:
        response_content, error = get_openai_response(tmp_path, VLLM_MODEL, OLLAMA_HOST, OLLAMA_KEY)
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
