from flask import Blueprint, request, jsonify
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from src.models import ApiDefinition, Base
import os
import json

# SQLite3 数据库文件路径
DB_PATH = os.getenv("API_DB_PATH", "sqlite:///ocr_api_management.db")
engine = create_engine(DB_PATH, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(bind=engine)

# 确保表结构已创建
Base.metadata.create_all(engine)

apis_api = Blueprint('apis_api', __name__)

@apis_api.route('/apis', methods=['POST'])
def create_api_definition():
    """
    保存 API 定义信息
    请求体: JSON { name, description, definition }
    """
    data = request.get_json()
    print("Received data:", data)
    
    if not data or 'name' not in data or 'definition' not in data:
        return jsonify({'error': '缺少必要参数 name 或 definition'}), 400
    
    name = data['name']
    description = data.get('description', '')
    definition = data['definition']
    
    session = SessionLocal()
    try:
        # 将 definition 转换为 JSON 字符串
        definition_json = json.dumps(definition)
        
        # 创建 API 定义记录
        api_def = ApiDefinition(name=name, description=description, definition=definition_json)
        session.add(api_def)
        session.commit()
        
        return jsonify({
            'message': 'API 定义已保存', 
            'id': api_def.id,
            'name': api_def.name
        }), 201
    except Exception as e:
        session.rollback()
        print("Error saving API definition:", str(e))
        return jsonify({'error': str(e)}), 500
    finally:
        session.close()

@apis_api.route('/apis', methods=['GET'])
def get_api_definitions():
    """
    获取所有 API 定义信息
    """
    session = SessionLocal()
    try:
        api_defs = session.query(ApiDefinition).all()
        result = []
        
        for api_def in api_defs:
            # 解析 JSON 字符串为 Python 对象
            try:
                definition = json.loads(api_def.definition)
            except:
                definition = {}
                
            result.append({
                'id': api_def.id,
                'name': api_def.name,
                'description': api_def.description,
                'definition': definition,
                'created_at': api_def.created_at.isoformat() if hasattr(api_def, 'created_at') else None
            })
            
        return jsonify(result), 200
    except Exception as e:
        print("Error fetching API definitions:", str(e))
        return jsonify({'error': str(e)}), 500
    finally:
        session.close()

@apis_api.route('/apis/<int:api_id>', methods=['GET'])
def get_api_definition(api_id):
    """
    获取指定 ID 的 API 定义
    """
    session = SessionLocal()
    try:
        api_def = session.query(ApiDefinition).filter(ApiDefinition.id == api_id).first()
        
        if not api_def:
            return jsonify({'error': f'API 定义 ID {api_id} 不存在'}), 404
            
        # 解析 JSON 字符串为 Python 对象
        try:
            definition = json.loads(api_def.definition)
        except:
            definition = {}
            
        result = {
            'id': api_def.id,
            'name': api_def.name,
            'description': api_def.description,
            'definition': definition,
            'created_at': api_def.created_at.isoformat() if hasattr(api_def, 'created_at') else None
        }
        
        return jsonify(result), 200
    except Exception as e:
        print(f"Error fetching API definition {api_id}:", str(e))
        return jsonify({'error': str(e)}), 500
    finally:
        session.close()

@apis_api.route('/apis/<int:api_id>', methods=['PUT'])
def update_api_definition(api_id):
    """
    更新指定 ID 的 API 定义
    """
    data = request.get_json()
    if not data or 'name' not in data or 'definition' not in data:
        return jsonify({'error': '缺少必要参数 name 或 definition'}), 400
    
    name = data['name']
    description = data.get('description', '')
    definition = data['definition']
    
    session = SessionLocal()
    try:
        api_def = session.query(ApiDefinition).filter(ApiDefinition.id == api_id).first()
        
        if not api_def:
            return jsonify({'error': f'API 定义 ID {api_id} 不存在'}), 404
        
        # 更新 API 定义
        api_def.name = name
        api_def.description = description
        api_def.definition = json.dumps(definition)
        
        session.commit()
        
        return jsonify({
            'message': f'API 定义 ID {api_id} 已更新',
            'id': api_def.id,
            'name': api_def.name
        }), 200
    except Exception as e:
        session.rollback()
        print(f"Error updating API definition {api_id}:", str(e))
        return jsonify({'error': str(e)}), 500
    finally:
        session.close()

@apis_api.route('/apis/<int:api_id>', methods=['DELETE'])
def delete_api_definition(api_id):
    """
    删除指定 ID 的 API 定义
    """
    session = SessionLocal()
    try:
        api_def = session.query(ApiDefinition).filter(ApiDefinition.id == api_id).first()
        
        if not api_def:
            return jsonify({'error': f'API 定义 ID {api_id} 不存在'}), 404
            
        session.delete(api_def)
        session.commit()
        
        return jsonify({'message': f'API 定义 ID {api_id} 已删除'}), 200
    except Exception as e:
        session.rollback()
        print(f"Error deleting API definition {api_id}:", str(e))
        return jsonify({'error': str(e)}), 500
    finally:
        session.close()