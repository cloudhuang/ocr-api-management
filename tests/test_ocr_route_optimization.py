"""
测试 OCR 路由查询优化的功能
"""
import pytest
import json
import tempfile
import os
from unittest.mock import patch, MagicMock
from src.router.ocr_route import ocr_api
from src.models import ApiDefinition, Base
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from flask import Flask


@pytest.fixture
def app():
    """创建测试用的 Flask 应用"""
    app = Flask(__name__)
    app.register_blueprint(ocr_api, url_prefix='/api')
    app.config['TESTING'] = True
    return app


@pytest.fixture
def client(app):
    """创建测试客户端"""
    return app.test_client()


@pytest.fixture
def test_db():
    """创建测试数据库"""
    # 使用内存数据库进行测试
    engine = create_engine("sqlite:///:memory:", connect_args={"check_same_thread": False})
    Base.metadata.create_all(engine)
    SessionLocal = sessionmaker(bind=engine)

    # 插入测试数据
    session = SessionLocal()
    try:
        test_api_def = ApiDefinition(
            api_code="TEST_001",
            name="测试API",
            description="这是一个测试API",
            definition=json.dumps({
                "apiCode": "TEST_001",
                "apiName": "测试OCR API",
                "project": "测试项目",
                "tags": ["ocr", "test"],
                "rules": ["返回JSON格式"],
                "responseFormat": "json",
                "jsonStructure": '{"text": "string", "confidence": "number"}'
            })
        )
        session.add(test_api_def)
        session.commit()
        
        # 添加另一个API定义用于测试查询精确性
        test_api_def2 = ApiDefinition(
            api_code="TEST_002",
            name="另一个测试API",
            description="这是另一个测试API",
            definition=json.dumps({
                "apiCode": "TEST_002",
                "apiName": "另一个OCR API",
                "project": "测试项目2",
                "tags": ["ocr", "test2"],
                "rules": ["返回Markdown格式"],
                "responseFormat": "markdown"
            })
        )
        session.add(test_api_def2)
        session.commit()
        
    finally:
        session.close()
    
    return engine, SessionLocal


def test_api_code_field_query_precision(test_db):
    """测试 api_code 字段查询的精确性"""
    engine, SessionLocal = test_db
    session = SessionLocal()

    try:
        # 测试精确匹配
        api_def = session.query(ApiDefinition).filter(
            ApiDefinition.api_code == "TEST_001"
        ).first()

        assert api_def is not None
        assert api_def.api_code == "TEST_001"
        assert api_def.name == "测试API"
        definition = json.loads(api_def.definition)
        assert definition['apiCode'] == "TEST_001"
        assert definition['apiName'] == "测试OCR API"

        # 测试不存在的 API CODE
        api_def_not_found = session.query(ApiDefinition).filter(
            ApiDefinition.api_code == "NONEXISTENT"
        ).first()

        assert api_def_not_found is None

        # 测试部分匹配不会返回错误结果
        api_def_partial = session.query(ApiDefinition).filter(
            ApiDefinition.api_code == "TEST"
        ).first()

        assert api_def_partial is None

        # 测试查询第二个API
        api_def2 = session.query(ApiDefinition).filter(
            ApiDefinition.api_code == "TEST_002"
        ).first()

        assert api_def2 is not None
        assert api_def2.api_code == "TEST_002"
        assert api_def2.name == "另一个测试API"

    finally:
        session.close()


def test_query_performance_comparison(test_db):
    """测试查询性能对比：优化前后的查询方式"""
    engine, SessionLocal = test_db
    session = SessionLocal()

    try:
        import time

        # 方法1：原始方法 - 查询所有记录然后遍历
        start_time = time.time()
        api_defs = session.query(ApiDefinition).all()
        matching_api_old = None
        for api_def in api_defs:
            try:
                definition = json.loads(api_def.definition)
                if definition.get('apiCode') == 'TEST_001':
                    matching_api_old = api_def
                    break
            except:
                continue
        old_method_time = time.time() - start_time

        # 方法2：优化后的方法 - 直接通过 api_code 字段查询
        start_time = time.time()
        matching_api_new = session.query(ApiDefinition).filter(
            ApiDefinition.api_code == 'TEST_001'
        ).first()
        new_method_time = time.time() - start_time

        # 验证结果一致性
        assert matching_api_old is not None
        assert matching_api_new is not None
        assert matching_api_old.id == matching_api_new.id

        # 输出性能对比（在实际数据量大的情况下，新方法会明显更快）
        print(f"\n性能对比:")
        print(f"原始方法耗时: {old_method_time:.6f}秒")
        print(f"优化方法耗时: {new_method_time:.6f}秒")
        print(f"性能提升: {((old_method_time - new_method_time) / old_method_time * 100):.2f}%")

    finally:
        session.close()


if __name__ == '__main__':
    pytest.main([__file__])
