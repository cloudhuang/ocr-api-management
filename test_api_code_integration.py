#!/usr/bin/env python3
"""
集成测试：验证 api_code 字段的完整功能
"""
import requests
import json
import tempfile
import os

BASE_URL = "http://localhost:8000"

def test_create_api_with_api_code():
    """测试创建带有 api_code 的 API 定义"""
    print("1. 测试创建 API 定义...")
    
    # 使用后端期望的数据格式
    api_data = {
        "name": "测试集成API",
        "description": "这是一个集成测试API",
        "definition": {
            "apiCode": "INTEGRATION_TEST_001",
            "apiName": "测试集成API",
            "description": "这是一个集成测试API",
            "project": "集成测试项目",
            "tags": ["integration", "test"],
            "rules": ["返回JSON格式", "包含置信度"],
            "responseFormat": "json",
            "jsonStructure": '{"text": "string", "confidence": "number"}'
        }
    }
    
    response = requests.post(f"{BASE_URL}/api/apis", json=api_data)
    print(f"创建API响应状态: {response.status_code}")
    
    if response.status_code == 201:
        result = response.json()
        print(f"创建成功: {result}")
        return result['id'], result['api_code']
    else:
        print(f"创建失败: {response.text}")
        return None, None

def test_get_api_definitions():
    """测试获取所有 API 定义"""
    print("\n2. 测试获取所有 API 定义...")
    
    response = requests.get(f"{BASE_URL}/api/apis")
    print(f"获取API列表响应状态: {response.status_code}")
    
    if response.status_code == 200:
        apis = response.json()
        print(f"找到 {len(apis)} 个API定义:")
        for api in apis:
            print(f"  - ID: {api['id']}, API Code: {api['api_code']}, Name: {api['name']}")
        return apis
    else:
        print(f"获取失败: {response.text}")
        return []

def test_ocr_with_api_code(api_code):
    """测试使用 api_code 进行 OCR 请求"""
    print(f"\n3. 测试使用 API Code '{api_code}' 进行 OCR 请求...")
    
    # 创建一个临时图片文件
    with tempfile.NamedTemporaryFile(suffix='.jpg', delete=False) as tmp_file:
        # 写入一些假的图片数据
        tmp_file.write(b'\xff\xd8\xff\xe0\x00\x10JFIF\x00\x01\x01\x01\x00H\x00H\x00\x00\xff\xdb\x00C\x00')
        tmp_file_path = tmp_file.name
    
    try:
        with open(tmp_file_path, 'rb') as f:
            files = {'image': ('test.jpg', f, 'image/jpeg')}
            data = {'api_code': api_code}
            
            response = requests.post(f"{BASE_URL}/api/ocr", files=files, data=data)
            print(f"OCR请求响应状态: {response.status_code}")
            
            if response.status_code == 200:
                result = response.json()
                print("OCR请求成功!")
                print(f"找到的API: {result['api']['name']}")
                print(f"API Code: {result['api']['definition']['apiCode']}")
                print(f"图片信息: {result['image']}")
                return True
            else:
                print(f"OCR请求失败: {response.text}")
                return False
    finally:
        os.unlink(tmp_file_path)

def test_ocr_with_nonexistent_api_code():
    """测试使用不存在的 api_code 进行 OCR 请求"""
    print("\n4. 测试使用不存在的 API Code 进行 OCR 请求...")
    
    with tempfile.NamedTemporaryFile(suffix='.jpg', delete=False) as tmp_file:
        tmp_file.write(b'\xff\xd8\xff\xe0\x00\x10JFIF\x00\x01\x01\x01\x00H\x00H\x00\x00\xff\xdb\x00C\x00')
        tmp_file_path = tmp_file.name
    
    try:
        with open(tmp_file_path, 'rb') as f:
            files = {'image': ('test.jpg', f, 'image/jpeg')}
            data = {'api_code': 'NONEXISTENT_CODE'}
            
            response = requests.post(f"{BASE_URL}/api/ocr", files=files, data=data)
            print(f"OCR请求响应状态: {response.status_code}")
            
            if response.status_code == 404:
                result = response.json()
                print(f"正确返回404错误: {result['error']}")
                return True
            else:
                print(f"意外的响应: {response.text}")
                return False
    finally:
        os.unlink(tmp_file_path)

def test_duplicate_api_code():
    """测试创建重复的 api_code"""
    print("\n5. 测试创建重复的 API Code...")
    
    # 使用后端期望的数据格式
    api_data = {
        "name": "重复测试API",
        "description": "这是一个重复API Code的测试",
        "definition": {
            "apiCode": "INTEGRATION_TEST_001",  # 使用相同的 API Code
            "apiName": "重复测试API",
            "description": "这是一个重复API Code的测试",
            "project": "重复测试项目",
            "tags": ["duplicate", "test"],
            "rules": ["测试重复"],
            "responseFormat": "json"
        }
    }
    
    response = requests.post(f"{BASE_URL}/api/apis", json=api_data)
    print(f"创建重复API响应状态: {response.status_code}")
    
    if response.status_code == 409:
        result = response.json()
        print(f"正确返回409冲突错误: {result['error']}")
        return True
    else:
        print(f"意外的响应: {response.text}")
        return False

def main():
    """主测试函数"""
    print("开始 API Code 字段集成测试...")
    print("=" * 50)
    
    # 1. 创建API定义
    api_id, api_code = test_create_api_with_api_code()
    if not api_id:
        print("创建API失败，终止测试")
        return
    
    # 2. 获取所有API定义
    apis = test_get_api_definitions()
    
    # 3. 使用正确的API Code进行OCR请求
    ocr_success = test_ocr_with_api_code(api_code)
    
    # 4. 使用不存在的API Code进行OCR请求
    not_found_success = test_ocr_with_nonexistent_api_code()
    
    # 5. 测试重复API Code
    duplicate_success = test_duplicate_api_code()
    
    # 总结
    print("\n" + "=" * 50)
    print("测试结果总结:")
    print(f"✅ 创建API: {'成功' if api_id else '失败'}")
    print(f"✅ 获取API列表: {'成功' if apis else '失败'}")
    print(f"✅ OCR请求: {'成功' if ocr_success else '失败'}")
    print(f"✅ 404错误处理: {'成功' if not_found_success else '失败'}")
    print(f"✅ 重复API Code处理: {'成功' if duplicate_success else '失败'}")
    
    all_success = all([api_id, apis, ocr_success, not_found_success, duplicate_success])
    print(f"\n🎉 总体测试结果: {'全部通过' if all_success else '部分失败'}")

if __name__ == "__main__":
    main()
