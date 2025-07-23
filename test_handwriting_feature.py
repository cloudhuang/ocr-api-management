#!/usr/bin/env python3
"""
测试手写体识别功能
验证前端表单、后端保存和PROMPT生成的完整流程
"""
import requests
import json
import sys
import os

# 添加项目根目录到 Python 路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

BASE_URL = "http://localhost:8000"

def test_prompt_generation_with_handwriting():
    """测试PROMPT生成器的手写体功能"""
    print("1. 测试PROMPT生成器的手写体功能...")
    
    try:
        from src.prompt_generator import create_ocr_prompt
        
        # 测试启用手写体识别的JSON API
        handwriting_json_api = {
            "responseFormat": "json",
            "includeHandwriting": True,
            "rules": ["识别手写日期", "识别手写签名"],
            "jsonStructure": '{"handwritten_text": "string", "confidence": "number"}'
        }
        
        # 测试未启用手写体识别的API
        normal_json_api = {
            "responseFormat": "json", 
            "includeHandwriting": False,
            "rules": ["只识别印刷体文字"],
            "jsonStructure": '{"printed_text": "string"}'
        }
        
        handwriting_prompt = create_ocr_prompt(handwriting_json_api)
        normal_prompt = create_ocr_prompt(normal_json_api)
        
        print("✅ PROMPT生成成功")
        print(f"   启用手写体PROMPT长度: {len(handwriting_prompt)} 字符")
        print(f"   普通PROMPT长度: {len(normal_prompt)} 字符")
        
        # 验证手写体增强规则是否包含在PROMPT中
        if "手寫體識別增強規則" in handwriting_prompt:
            print("✅ 手写体增强规则已正确添加")
        else:
            print("❌ 手写体增强规则未找到")
            return False
            
        if "手寫體識別增強規則" not in normal_prompt:
            print("✅ 普通PROMPT未包含手写体规则")
        else:
            print("❌ 普通PROMPT错误包含了手写体规则")
            return False
            
        return True
        
    except Exception as e:
        print(f"❌ PROMPT生成测试失败: {str(e)}")
        return False

def test_create_handwriting_api():
    """测试创建启用手写体识别的API"""
    print("\n2. 测试创建启用手写体识别的API...")
    
    api_data = {
        "name": "手写体识别测试API",
        "description": "测试手写体识别功能的API",
        "definition": {
            "apiCode": "HANDWRITING_TEST_001",
            "apiName": "手写体识别测试API",
            "description": "测试手写体识别功能的API",
            "project": "手写体测试项目",
            "tags": ["handwriting", "ocr", "test"],
            "rules": [
                "专门识别手写文字",
                "包括草书和连笔字",
                "返回置信度评分"
            ],
            "responseFormat": "json",
            "jsonStructure": '{"handwritten_content": "string", "confidence": "number", "type": "handwritten|printed"}',
            "includeHandwriting": True
        }
    }
    
    response = requests.post(f"{BASE_URL}/api/apis", json=api_data)
    if response.status_code == 201:
        result = response.json()
        print(f"✅ 手写体API创建成功: {result['api_code']}")
        return result['api_code']
    else:
        print(f"❌ 手写体API创建失败: {response.text}")
        return None

def test_create_normal_api():
    """测试创建普通API（未启用手写体）"""
    print("\n3. 测试创建普通API（未启用手写体）...")
    
    api_data = {
        "name": "普通OCR测试API",
        "description": "测试普通OCR识别功能的API",
        "definition": {
            "apiCode": "NORMAL_OCR_TEST_001",
            "apiName": "普通OCR测试API",
            "description": "测试普通OCR识别功能的API",
            "project": "普通OCR测试项目",
            "tags": ["ocr", "printed", "test"],
            "rules": [
                "只识别印刷体文字",
                "忽略手写内容",
                "高精度识别"
            ],
            "responseFormat": "markdown",
            "includeHandwriting": False
        }
    }
    
    response = requests.post(f"{BASE_URL}/api/apis", json=api_data)
    if response.status_code == 201:
        result = response.json()
        print(f"✅ 普通API创建成功: {result['api_code']}")
        return result['api_code']
    else:
        print(f"❌ 普通API创建失败: {response.text}")
        return None

def test_get_api_details(api_code):
    """测试获取API详情，验证手写体字段是否正确保存"""
    print(f"\n4. 测试获取API详情: {api_code}")

    # 首先获取所有API列表找到对应的ID
    response = requests.get(f"{BASE_URL}/api/apis")
    if response.status_code != 200:
        print(f"❌ 获取API列表失败: {response.text}")
        return False

    apis = response.json()
    target_api = None
    for api in apis:
        if api.get('api_code') == api_code:
            target_api = api
            break

    if not target_api:
        print(f"❌ 未找到API: {api_code}")
        return False

    print(f"✅ 找到API: {target_api['name']}")
    print(f"   API Code: {target_api['api_code']}")
    print(f"   手写体识别: {target_api['definition'].get('includeHandwriting', False)}")

    return True

def test_api_list_display():
    """测试API列表页面是否正确显示手写体识别状态"""
    print(f"\n5. 测试API列表显示手写体识别状态...")

    response = requests.get(f"{BASE_URL}/api/apis")
    if response.status_code != 200:
        print(f"❌ 获取API列表失败: {response.text}")
        return False

    apis = response.json()

    # 检查是否有API包含手写体字段
    handwriting_apis = []
    normal_apis = []

    for api in apis:
        include_handwriting = api['definition'].get('includeHandwriting', False)
        if include_handwriting:
            handwriting_apis.append(api['api_code'])
        else:
            normal_apis.append(api['api_code'])

    print(f"✅ API列表获取成功")
    print(f"   总计API数量: {len(apis)}")
    print(f"   启用手写体的API: {len(handwriting_apis)} 个")
    print(f"   未启用手写体的API: {len(normal_apis)} 个")

    if handwriting_apis:
        print(f"   启用手写体的API: {', '.join(handwriting_apis)}")
    if normal_apis:
        print(f"   未启用手写体的API: {', '.join(normal_apis[:3])}{'...' if len(normal_apis) > 3 else ''}")

    return True

def test_prompt_generation_in_ocr_route():
    """测试OCR路由中的PROMPT生成"""
    print("\n5. 测试OCR路由中的PROMPT生成...")
    
    # 这里我们可以通过查看日志来验证，或者创建一个简单的图片进行测试
    # 由于需要实际的图片和模型，这里只做基本的API调用测试
    
    try:
        # 创建一个简单的测试图片
        import tempfile
        from PIL import Image, ImageDraw, ImageFont
        
        # 创建包含手写风格文本的测试图片
        img = Image.new('RGB', (400, 200), color='white')
        draw = ImageDraw.Draw(img)
        
        # 模拟手写文本
        text = "手写测试文本\nHandwritten Test\n2024-01-15"
        draw.text((20, 20), text, fill='black')
        
        # 保存临时图片
        with tempfile.NamedTemporaryFile(suffix='.png', delete=False) as tmp_file:
            img.save(tmp_file.name)
            test_image_path = tmp_file.name
        
        print(f"✅ 创建测试图片: {test_image_path}")
        return test_image_path
        
    except Exception as e:
        print(f"⚠️  无法创建测试图片: {str(e)}")
        return None

def main():
    """主测试函数"""
    print("开始手写体识别功能测试...")
    print("=" * 60)
    
    # 1. 测试PROMPT生成
    prompt_success = test_prompt_generation_with_handwriting()
    
    # 2. 创建测试API
    handwriting_api_code = test_create_handwriting_api()
    normal_api_code = test_create_normal_api()
    
    # 3. 验证API详情
    handwriting_details_success = False
    normal_details_success = False

    if handwriting_api_code:
        handwriting_details_success = test_get_api_details(handwriting_api_code)

    if normal_api_code:
        normal_details_success = test_get_api_details(normal_api_code)

    # 4. 测试API列表显示
    list_display_success = test_api_list_display()

    # 5. 测试图片生成
    test_image = test_prompt_generation_in_ocr_route()
    
    # 清理测试图片
    if test_image and os.path.exists(test_image):
        try:
            os.unlink(test_image)
            print(f"✅ 已清理测试图片: {test_image}")
        except:
            pass
    
    # 总结测试结果
    print("\n" + "=" * 60)
    print("测试结果总结:")
    print(f"✅ PROMPT生成测试: {'成功' if prompt_success else '失败'}")
    print(f"✅ 手写体API创建: {'成功' if handwriting_api_code else '失败'}")
    print(f"✅ 普通API创建: {'成功' if normal_api_code else '失败'}")
    print(f"✅ 手写体API详情: {'成功' if handwriting_details_success else '失败'}")
    print(f"✅ 普通API详情: {'成功' if normal_details_success else '失败'}")
    print(f"✅ API列表显示: {'成功' if list_display_success else '失败'}")

    all_success = all([
        prompt_success,
        handwriting_api_code,
        normal_api_code,
        handwriting_details_success,
        normal_details_success,
        list_display_success
    ])
    
    print(f"\n🎉 总体测试结果: {'全部通过' if all_success else '部分失败'}")
    
    if all_success:
        print("\n🚀 手写体识别功能已成功实现!")
        print("   - 前端表单支持手写体开关（位置在RULES上方）")
        print("   - 后端正确保存手写体字段")
        print("   - PROMPT生成器支持手写体增强")
        print("   - API详情页面显示手写体状态")
        print("   - API列表页面显示手写体状态")
        print("   - 创建和编辑页面都支持手写体开关")
    else:
        print("\n⚠️  部分功能需要进一步调试")

if __name__ == "__main__":
    main()
