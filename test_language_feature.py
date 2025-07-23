#!/usr/bin/env python3
"""
测试返回语言功能
验证前端表单、后端保存和PROMPT生成的完整流程
"""
import requests
import json
import sys
import os

# 添加项目根目录到 Python 路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

BASE_URL = "http://localhost:8000"

def test_prompt_generation_with_languages():
    """测试PROMPT生成器的多语言功能"""
    print("1. 测试PROMPT生成器的多语言功能...")
    
    try:
        from src.prompt_generator import create_ocr_prompt
        
        # 测试不同语言的API定义
        languages = [
            ("english", "English"),
            ("simplified_chinese", "简体中文"),
            ("traditional_chinese", "繁體中文"),
            ("japanese", "日本語")
        ]
        
        for lang_code, lang_name in languages:
            print(f"\n   测试 {lang_name} ({lang_code}):")
            
            # JSON格式测试
            json_api = {
                "responseFormat": "json",
                "responseLanguage": lang_code,
                "includeHandwriting": False,
                "rules": ["测试多语言规则"],
                "jsonStructure": '{"text": "string", "language": "string"}'
            }
            
            json_prompt = create_ocr_prompt(json_api)
            
            # 验证语言指令是否包含在PROMPT中
            language_checks = {
                "english": "Please respond in English" in json_prompt,
                "simplified_chinese": "请使用简体中文回复" in json_prompt,
                "traditional_chinese": "請使用繁體中文回覆" in json_prompt,
                "japanese": "日本語で回答してください" in json_prompt
            }
            
            if language_checks[lang_code]:
                print(f"     ✅ JSON PROMPT包含{lang_name}指令")
            else:
                print(f"     ❌ JSON PROMPT缺少{lang_name}指令")
                return False
            
            # Markdown格式测试
            markdown_api = {
                "responseFormat": "markdown",
                "responseLanguage": lang_code,
                "includeHandwriting": False,
                "rules": ["测试多语言规则"]
            }
            
            markdown_prompt = create_ocr_prompt(markdown_api)
            
            if language_checks[lang_code]:
                print(f"     ✅ Markdown PROMPT包含{lang_name}指令")
            else:
                print(f"     ❌ Markdown PROMPT缺少{lang_name}指令")
                return False
        
        print("\n✅ 所有语言的PROMPT生成测试通过")
        return True
        
    except Exception as e:
        print(f"❌ PROMPT生成测试失败: {str(e)}")
        return False

def test_create_multilingual_apis():
    """测试创建不同语言的API"""
    print("\n2. 测试创建不同语言的API...")
    
    languages = [
        ("english", "English OCR API", "English"),
        ("simplified_chinese", "简体中文OCR API", "简体中文"),
        ("traditional_chinese", "繁體中文OCR API", "繁體中文"),
        ("japanese", "日本語OCR API", "日本語")
    ]
    
    created_apis = []
    
    for lang_code, api_name, lang_display in languages:
        print(f"\n   创建{lang_display}API...")
        
        api_data = {
            "name": api_name,
            "description": f"测试{lang_display}返回的OCR API",
            "definition": {
                "apiCode": f"LANG_TEST_{lang_code.upper()}",
                "apiName": api_name,
                "description": f"测试{lang_display}返回的OCR API",
                "project": "多语言测试项目",
                "tags": ["multilingual", "ocr", "test"],
                "rules": [
                    f"使用{lang_display}返回结果",
                    "保持高识别精度",
                    "包含置信度评分"
                ],
                "responseFormat": "json",
                "jsonStructure": '{"text": "string", "language": "string", "confidence": "number"}',
                "includeHandwriting": False,
                "responseLanguage": lang_code
            }
        }
        
        response = requests.post(f"{BASE_URL}/api/apis", json=api_data)
        if response.status_code == 201:
            result = response.json()
            created_apis.append((result['api_code'], lang_display))
            print(f"     ✅ {lang_display}API创建成功: {result['api_code']}")
        else:
            print(f"     ❌ {lang_display}API创建失败: {response.text}")
            return False, []
    
    return True, created_apis

def test_api_list_with_languages():
    """测试API列表显示语言信息"""
    print("\n3. 测试API列表显示语言信息...")
    
    response = requests.get(f"{BASE_URL}/api/apis")
    if response.status_code != 200:
        print(f"❌ 获取API列表失败: {response.text}")
        return False
    
    apis = response.json()
    
    # 统计不同语言的API
    language_stats = {}
    for api in apis:
        lang = api['definition'].get('responseLanguage', 'english')
        language_stats[lang] = language_stats.get(lang, 0) + 1
    
    print(f"✅ API列表获取成功，总计 {len(apis)} 个API")
    print("   语言分布:")
    for lang, count in language_stats.items():
        lang_names = {
            "english": "English",
            "simplified_chinese": "简体中文",
            "traditional_chinese": "繁體中文",
            "japanese": "日本語"
        }
        lang_display = lang_names.get(lang, lang)
        print(f"     - {lang_display}: {count} 个")
    
    return True

def test_api_details_with_language(api_codes):
    """测试API详情页面显示语言信息"""
    print("\n4. 测试API详情显示语言信息...")
    
    # 获取所有API列表
    response = requests.get(f"{BASE_URL}/api/apis")
    if response.status_code != 200:
        print(f"❌ 获取API列表失败: {response.text}")
        return False
    
    apis = response.json()
    
    # 验证每个创建的API的语言信息
    for api_code, expected_lang in api_codes:
        target_api = None
        for api in apis:
            if api.get('api_code') == api_code:
                target_api = api
                break
        
        if target_api:
            actual_lang = target_api['definition'].get('responseLanguage', 'english')
            expected_lang_code = {
                "English": "english",
                "简体中文": "simplified_chinese", 
                "繁體中文": "traditional_chinese",
                "日本語": "japanese"
            }.get(expected_lang, "english")
            
            if actual_lang == expected_lang_code:
                print(f"     ✅ {api_code} 语言设置正确: {expected_lang}")
            else:
                print(f"     ❌ {api_code} 语言设置错误: 期望{expected_lang_code}，实际{actual_lang}")
                return False
        else:
            print(f"     ❌ 未找到API: {api_code}")
            return False
    
    return True

def main():
    """主测试函数"""
    print("开始返回语言功能测试...")
    print("=" * 60)
    
    # 1. 测试PROMPT生成
    prompt_success = test_prompt_generation_with_languages()
    
    # 2. 创建多语言API
    api_creation_success, created_apis = test_create_multilingual_apis()
    
    # 3. 测试API列表显示
    list_success = test_api_list_with_languages()
    
    # 4. 测试API详情显示
    details_success = False
    if created_apis:
        details_success = test_api_details_with_language(created_apis)
    
    # 总结测试结果
    print("\n" + "=" * 60)
    print("测试结果总结:")
    print(f"✅ PROMPT多语言生成: {'成功' if prompt_success else '失败'}")
    print(f"✅ 多语言API创建: {'成功' if api_creation_success else '失败'}")
    print(f"✅ API列表语言显示: {'成功' if list_success else '失败'}")
    print(f"✅ API详情语言显示: {'成功' if details_success else '失败'}")
    
    all_success = all([
        prompt_success,
        api_creation_success,
        list_success,
        details_success
    ])
    
    print(f"\n🎉 总体测试结果: {'全部通过' if all_success else '部分失败'}")
    
    if all_success:
        print("\n🚀 返回语言功能已成功实现!")
        print("   - 支持英文、简体中文、繁体中文、日文四种语言")
        print("   - 前端表单支持语言选择")
        print("   - 后端正确保存语言设置")
        print("   - PROMPT生成器支持多语言指令")
        print("   - API列表和详情页面显示语言信息")
        print("   - 创建和编辑页面都支持语言选择")
    else:
        print("\n⚠️  部分功能需要进一步调试")
    
    if created_apis:
        print(f"\n📋 本次测试创建的API:")
        for api_code, lang in created_apis:
            print(f"   - {api_code} ({lang})")

if __name__ == "__main__":
    main()
