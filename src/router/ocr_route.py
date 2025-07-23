from flask import Blueprint, request, jsonify
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from src.models import ApiDefinition, Base
from src.prompt_generator import create_ocr_prompt
from src.llm_client import get_openai_response
from src.config import VLLM_MODEL, OLLAMA_HOST, OLLAMA_KEY
import os
import json
import logging
import tempfile
import time

# 配置日志
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# SQLite3 数据库文件路径
DB_PATH = os.getenv("API_DB_PATH", "sqlite:///ocr_api_management.db")
engine = create_engine(DB_PATH, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(bind=engine)

# 确保表结构已创建
Base.metadata.create_all(engine)

ocr_api = Blueprint('ocr_api', __name__)

@ocr_api.route('/ocr', methods=['POST'])
def process_ocr():
    """
    OCR 处理接口
    接受参数:
    - api_code: API 代码，用于查询 API 定义
    - image: 图片文件
    """
    # 检查是否有 API CODE
    api_code = request.form.get('api_code')
    if not api_code:
        return jsonify({'error': '缺少必要参数 api_code'}), 400
    
    # 检查是否有图片文件
    if 'image' not in request.files:
        return jsonify({'error': '缺少图片文件'}), 400
    
    image_file = request.files['image']
    if image_file.filename == '':
        return jsonify({'error': '未选择图片文件'}), 400
    
    # 通过 API CODE 查询 API 定义
    session = SessionLocal()
    try:
        # 直接通过 api_code 字段查询 API 定义
        # 使用专门的字段查询，性能更好且兼容所有数据库
        api_def = session.query(ApiDefinition).filter(
            ApiDefinition.api_code == api_code
        ).first()

        if not api_def:
            return jsonify({'error': f'未找到 API CODE 为 {api_code} 的 API 定义'}), 404

        # 解析找到的 API 定义
        try:
            definition = json.loads(api_def.definition)
            matching_api = {
                'id': api_def.id,
                'name': api_def.name,
                'description': api_def.description,
                'definition': definition
            }
        except Exception as e:
            logger.error(f"Error parsing API definition: {str(e)}")
            return jsonify({'error': 'API 定义格式错误'}), 500
        
        # 打印 API 定义到控制台
        logger.info(f"Found API definition for code {api_code}:")
        logger.info(f"API ID: {matching_api['id']}")
        logger.info(f"API Name: {matching_api['name']}")
        logger.info(f"API Description: {matching_api['description']}")
        logger.info(f"API Definition: {json.dumps(matching_api['definition'], indent=2)}")
        
        # 获取图片信息
        filename = image_file.filename
        file_size = 0
        image_file.seek(0, os.SEEK_END)
        file_size = image_file.tell()
        image_file.seek(0)  # 重置文件指针

        logger.info(f"Received image: {filename}, size: {file_size} bytes")

        # 保存临时图片文件
        with tempfile.NamedTemporaryFile(delete=False, suffix='.jpg') as tmp_file:
            image_file.save(tmp_file.name)
            tmp_image_path = tmp_file.name

        try:
            # 根据API定义生成PROMPT
            custom_prompt = create_ocr_prompt(matching_api['definition'])
            logger.info(f"Generated custom prompt for API {api_code}")

            # 调用OCR推理
            logger.info(f"Starting OCR inference with model {VLLM_MODEL}")
            start_time = time.time()

            ocr_result, error = get_openai_response(
                image_path=tmp_image_path,
                model=VLLM_MODEL,
                host=OLLAMA_HOST,
                key=OLLAMA_KEY,
                prompt=custom_prompt
            )

            inference_time = time.time() - start_time
            logger.info(f"OCR inference completed in {inference_time:.2f} seconds")

            if error:
                logger.error(f"OCR inference failed: {error}")
                return jsonify({'error': f'OCR 推理失败: {error}'}), 500

            # 尝试解析结果（如果是JSON格式）
            parsed_result = None
            response_format = matching_api['definition'].get('responseFormat', 'json')

            if response_format.lower() == 'json':
                try:
                    # 清理可能的markdown标记
                    cleaned_result = ocr_result.strip()
                    if cleaned_result.startswith('```json'):
                        cleaned_result = cleaned_result[7:]
                    if cleaned_result.endswith('```'):
                        cleaned_result = cleaned_result[:-3]
                    cleaned_result = cleaned_result.strip()

                    parsed_result = json.loads(cleaned_result)
                    logger.info("Successfully parsed JSON result")
                except json.JSONDecodeError as e:
                    logger.warning(f"Failed to parse JSON result: {e}")
                    # 如果解析失败，仍然返回原始结果
                    parsed_result = {"raw_text": ocr_result, "parse_error": str(e)}

            # 返回OCR结果
            return jsonify({
                'message': 'OCR 处理完成',
                'api': {
                    'id': matching_api['id'],
                    'api_code': api_code,
                    'name': matching_api['name'],
                    'response_format': response_format
                },
                'image': {
                    'filename': filename,
                    'size': file_size
                },
                'ocr_result': {
                    'raw_text': ocr_result,
                    'parsed_result': parsed_result,
                    'inference_time': round(inference_time, 2)
                }
            }), 200

        finally:
            # 清理临时文件
            try:
                os.unlink(tmp_image_path)
                logger.info(f"Cleaned up temporary file: {tmp_image_path}")
            except Exception as e:
                logger.warning(f"Failed to clean up temporary file: {e}")
        
    except Exception as e:
        logger.error(f"Error processing OCR request: {str(e)}")
        return jsonify({'error': str(e)}), 500
    finally:
        session.close()