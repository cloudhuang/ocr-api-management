#!/usr/bin/env python3
"""
测试优化后的PROMPT生成器
验证JSON和Markdown格式的PROMPT是否正确分离和优化
"""
import sys
import os

# 添加项目根目录到 Python 路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from src.prompt_generator import OCRPromptGenerator, create_ocr_prompt

def test_json_prompt_generation():
    """测试JSON格式PROMPT生成"""
    print("1. 测试JSON格式PROMPT生成...")
    
    generator = OCRPromptGenerator()
    
    # 测试基础JSON API（无手写体）
    basic_json_api = {
        "responseFormat": "json",
        "includeHandwriting": False,
        "rules": ["返回日期格式为 yyyy-MM-dd", "金额必须包含货币符号"],
        "jsonStructure": '{"invoice_number": "string", "date": "string", "amount": "string"}'
    }
    
    basic_prompt = generator.generate_json_prompt(basic_json_api)
    
    print("✅ 基础JSON PROMPT生成成功")
    print(f"   长度: {len(basic_prompt)} 字符")
    
    # 验证关键内容
    checks = [
        ("包含JSON基础提示词", "AI文档识别服务" in basic_prompt),
        ("包含JSON格式要求", "JSON格式" in basic_prompt),
        ("包含用户规则", "用户自定义规则" in basic_prompt),
        ("包含自定义JSON结构", "invoice_number" in basic_prompt),
        ("不包含手写体规则", "手写体识别增强规则" not in basic_prompt),
        ("不包含Markdown相关内容", "Markdown" not in basic_prompt)
    ]
    
    for check_name, result in checks:
        status = "✅" if result else "❌"
        print(f"   {status} {check_name}")
    
    return all(result for _, result in checks)

def test_json_prompt_with_handwriting():
    """测试启用手写体的JSON格式PROMPT"""
    print("\n2. 测试启用手写体的JSON格式PROMPT...")
    
    generator = OCRPromptGenerator()
    
    handwriting_json_api = {
        "responseFormat": "json",
        "includeHandwriting": True,
        "rules": ["识别手写签名", "手写日期转换为标准格式"],
        "jsonStructure": '{"handwritten_text": "string", "signature": "string", "confidence": "number"}'
    }
    
    handwriting_prompt = generator.generate_json_prompt(handwriting_json_api)
    
    print("✅ 手写体JSON PROMPT生成成功")
    print(f"   长度: {len(handwriting_prompt)} 字符")
    
    # 验证关键内容
    checks = [
        ("包含JSON基础提示词", "AI文档识别服务" in handwriting_prompt),
        ("包含手写体增强规则", "手写体识别增强规则" in handwriting_prompt),
        ("包含手写体专注", "手写体专注" in handwriting_prompt),
        ("包含用户规则", "识别手写签名" in handwriting_prompt),
        ("包含自定义JSON结构", "handwritten_text" in handwriting_prompt)
    ]
    
    for check_name, result in checks:
        status = "✅" if result else "❌"
        print(f"   {status} {check_name}")
    
    return all(result for _, result in checks)

def test_markdown_prompt_generation():
    """测试Markdown格式PROMPT生成"""
    print("\n3. 测试Markdown格式PROMPT生成...")
    
    generator = OCRPromptGenerator()
    
    # 测试基础Markdown API（无手写体）
    basic_markdown_api = {
        "responseFormat": "markdown",
        "includeHandwriting": False,
        "rules": ["保持原始表格格式", "使用标准Markdown语法"]
    }
    
    basic_prompt = generator.generate_markdown_prompt(basic_markdown_api)
    
    print("✅ 基础Markdown PROMPT生成成功")
    print(f"   长度: {len(basic_prompt)} 字符")
    
    # 验证关键内容
    checks = [
        ("包含Markdown基础提示词", "AI文档识别服务" in basic_prompt),
        ("包含Markdown格式要求", "Markdown格式" in basic_prompt),
        ("包含表格语法说明", "表格语法" in basic_prompt),
        ("包含用户规则", "保持原始表格格式" in basic_prompt),
        ("不包含手写体规则", "手写体识别增强规则" not in basic_prompt),
        ("不包含JSON相关内容", "JSON" not in basic_prompt)
    ]
    
    for check_name, result in checks:
        status = "✅" if result else "❌"
        print(f"   {status} {check_name}")
    
    return all(result for _, result in checks)

def test_markdown_prompt_with_handwriting():
    """测试启用手写体的Markdown格式PROMPT"""
    print("\n4. 测试启用手写体的Markdown格式PROMPT...")
    
    generator = OCRPromptGenerator()
    
    handwriting_markdown_api = {
        "responseFormat": "markdown",
        "includeHandwriting": True,
        "rules": ["识别手写表格内容", "保持手写文字的原始格式"]
    }
    
    handwriting_prompt = generator.generate_markdown_prompt(handwriting_markdown_api)
    
    print("✅ 手写体Markdown PROMPT生成成功")
    print(f"   长度: {len(handwriting_prompt)} 字符")
    
    # 验证关键内容
    checks = [
        ("包含Markdown基础提示词", "AI文档识别服务" in handwriting_prompt),
        ("包含手写体增强规则", "手写体识别增强规则" in handwriting_prompt),
        ("包含Markdown格式要求", "Markdown格式" in handwriting_prompt),
        ("包含用户规则", "识别手写表格内容" in handwriting_prompt)
    ]
    
    for check_name, result in checks:
        status = "✅" if result else "❌"
        print(f"   {status} {check_name}")
    
    return all(result for _, result in checks)

def test_prompt_separation():
    """测试PROMPT的分离性"""
    print("\n5. 测试PROMPT格式分离...")
    
    generator = OCRPromptGenerator()
    
    # 生成两种格式的PROMPT
    json_api = {"responseFormat": "json", "includeHandwriting": False, "rules": ["测试规则"]}
    markdown_api = {"responseFormat": "markdown", "includeHandwriting": False, "rules": ["测试规则"]}
    
    json_prompt = generator.generate_json_prompt(json_api)
    markdown_prompt = generator.generate_markdown_prompt(markdown_api)
    
    # 验证分离性
    checks = [
        ("JSON PROMPT不包含Markdown内容", "Markdown" not in json_prompt),
        ("Markdown PROMPT不包含JSON内容", "JSON" not in markdown_prompt),
        ("两种PROMPT基础内容不同", json_prompt[:100] != markdown_prompt[:100]),
        ("JSON PROMPT包含JSON特定要求", "JSON格式" in json_prompt),
        ("Markdown PROMPT包含Markdown特定要求", "Markdown格式" in markdown_prompt)
    ]
    
    for check_name, result in checks:
        status = "✅" if result else "❌"
        print(f"   {status} {check_name}")
    
    return all(result for _, result in checks)

def test_convenience_function():
    """测试便捷函数"""
    print("\n6. 测试便捷函数...")
    
    test_api = {
        "responseFormat": "json",
        "includeHandwriting": True,
        "rules": ["测试便捷函数"],
        "jsonStructure": '{"test": "string"}'
    }
    
    prompt = create_ocr_prompt(test_api)
    
    checks = [
        ("便捷函数正常工作", len(prompt) > 0),
        ("包含测试规则", "测试便捷函数" in prompt),
        ("包含手写体规则", "手写体识别增强规则" in prompt)
    ]
    
    for check_name, result in checks:
        status = "✅" if result else "❌"
        print(f"   {status} {check_name}")
    
    return all(result for _, result in checks)

def main():
    """主测试函数"""
    print("开始PROMPT生成器优化测试...")
    print("=" * 60)
    
    # 执行所有测试
    test_results = [
        test_json_prompt_generation(),
        test_json_prompt_with_handwriting(),
        test_markdown_prompt_generation(),
        test_markdown_prompt_with_handwriting(),
        test_prompt_separation(),
        test_convenience_function()
    ]
    
    # 总结测试结果
    print("\n" + "=" * 60)
    print("测试结果总结:")
    test_names = [
        "基础JSON PROMPT生成",
        "手写体JSON PROMPT生成", 
        "基础Markdown PROMPT生成",
        "手写体Markdown PROMPT生成",
        "PROMPT格式分离",
        "便捷函数测试"
    ]
    
    for i, (name, result) in enumerate(zip(test_names, test_results)):
        status = "✅ 成功" if result else "❌ 失败"
        print(f"{status} {name}")
    
    all_success = all(test_results)
    print(f"\n🎉 总体测试结果: {'全部通过' if all_success else '部分失败'}")
    
    if all_success:
        print("\n🚀 PROMPT生成器优化成功!")
        print("   - JSON和Markdown格式完全分离")
        print("   - 手写体增强规则正确集成")
        print("   - 用户自定义规则正确处理")
        print("   - 基础提示词针对格式优化")
        print("   - 不再混合使用prompts.py的内容")
    else:
        print("\n⚠️  部分功能需要进一步调试")

if __name__ == "__main__":
    main()
