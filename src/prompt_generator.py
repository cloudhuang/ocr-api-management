"""
OCR PROMPT 生成器
根据API定义动态生成不同格式的PROMPT
"""
import json
from typing import Dict, List, Any


class OCRPromptGenerator:
    """OCR PROMPT 生成器类"""

    def __init__(self):
        # 语言配置
        self.language_configs = {
            "english": {
                "name": "English",
                "instruction": "You must respond in English only. If the original text is in Chinese, Japanese, or other languages, translate ALL content to English after preserving the document structure and return the translated content.",
                "date_format": "yyyy-MM-dd",
                "currency_note": "Keep original currency symbols",
                "translation_note": "Translate ALL field names and content to English. Do not leave any Chinese or Japanese text untranslated."
            },
            "simplified_chinese": {
                "name": "简体中文",
                "instruction": "必须使用简体中文回复。如果原文是英文、日文或其他语言，请将所有识别出来的内容翻译为简体中文，并用中文回复，同时保持文档结构。",
                "date_format": "yyyy年MM月dd日 或 yyyy-MM-dd",
                "currency_note": "保持原有货币符号",
                "translation_note": "将所有字段名称和内容翻译为简体中文。不要保留英文或日文原文。"
            },
            "traditional_chinese": {
                "name": "繁體中文",
                "instruction": "必須使用繁體中文回覆。如果原文是英文、日文或其他語言，請將所有識別出來的內容翻譯為繁體中文，並用繁體中文回復，同時保持文檔結構。",
                "date_format": "yyyy年MM月dd日 或 yyyy-MM-dd",
                "currency_note": "保持原有貨幣符號",
                "translation_note": "將所有欄位名稱和內容翻譯為繁體中文。不要保留英文或日文原文。"
            },
            "japanese": {
                "name": "日本語",
                "instruction": "必ず日本語で回答してください。元のテキストが英語や中国語などの他の言語である場合は、すべて認識できる内容を日本語に翻訳し、日本語で返信してください。文書の構造はそのまま保持してください。",
                "date_format": "yyyy年MM月dd日 または yyyy-MM-dd",
                "currency_note": "元の通貨記号を保持",
                "translation_note": "すべてのフィールド名、内容、テキストを日本語に翻訳してください。英語や中国語をそのまま残さないでください。"
            }
        }

        # JSON格式的基础提示词
        self.json_base_prompt = """你是一个高精度的AI文档识别服务。你的任务是分析提供的图片，识别其中的文字内容，并按照指定的JSON格式返回结果。

**核心指令：**
- 仔细分析图片中的所有文字内容（包括印刷体和手写体）
- 识别表格、表单、文档中的各个字段和对应的值
- 按照指定的JSON结构组织识别结果
- 所有输出必须基于图片中的视觉证据

**识别准确性规则：**
1. **高置信度原则**：只输出你确信正确的内容
2. **严禁猜测**：不确定的内容标记为无法识别，不要编造
3. **空白处理**：完全空白的字段返回空字符串 ""
4. **无法识别处理**：模糊不清的内容返回 "[UNRECOGNIZABLE]"
"""

        # Markdown格式的基础提示词
        self.markdown_base_prompt = """你是一个高精度的AI文档识别服务。你的任务是分析提供的图片，识别其中的文字内容，并以Markdown格式返回结果。

**核心指令：**
- 仔细分析图片中的所有文字内容（包括印刷体和手写体）
- 保持原始文档的结构和格式
- 使用标准的Markdown语法组织内容
- 所有输出必须基于图片中的视觉证据

**格式化规则：**
1. **标题层级**：使用 # ## ### 表示不同级别的标题
2. **表格格式**：使用标准Markdown表格语法 | 列1 | 列2 |
3. **列表格式**：使用 - 或 1. 表示列表项
4. **强调文本**：使用 **粗体** 或 *斜体* 标记重要内容
5. **保持结构**：尽量保持原文档的视觉结构和层次

**识别准确性规则：**
1. **高置信度原则**：只输出你确信正确的内容
2. **严禁猜测**：不确定的内容用 [无法识别] 标记
3. **保持格式**：严格遵循原文档的格式布局"""

        # 手写体增强规则
        self.handwriting_enhancement = """

**手写体识别增强规则：**
1. **手写体专注**：特别注意图片中的手写文字，包括草书、连笔字、个人笔迹等
2. **笔迹分析**：仔细分析笔画的连接、字符的形状变化，即使字迹不工整也要尽力识别
3. **上下文推理**：利用周围的印刷体文字和表格结构来辅助理解手写内容
4. **常见模式**：识别常见的手写数字、日期、姓名、签名等模式
5. **多种可能性**：如果手写字迹有歧义，在备注中提供可能的替代解释
6. **签名处理**：签名字段返回 "[SIGNATURE]"（除非是清晰的正楷字）
7. **手写特殊处理**：
   - 模糊手写内容：返回 "[UNRECOGNIZABLE]"
   - 签名字段：返回 "[SIGNATURE]"（除非是清晰正楷）
   - 手写日期：尽量识别并转换为标准格式"""

    def _get_language_instruction(self, language: str) -> str:
        """获取语言指令"""
        config = self.language_configs.get(language, self.language_configs["english"])
        return f"""

**语言要求：**
- {config["instruction"]}
- 翻译说明：{config["translation_note"]}
- 日期格式：{config["date_format"]}
- 货币处理：{config["currency_note"]}"""

    def generate_json_prompt(self, api_definition: Dict[str, Any]) -> str:
        """生成JSON格式的PROMPT"""

        # 提取用户规则
        rules = api_definition.get('rules', [])
        user_rules = self._format_user_rules(rules)

        # 检查是否启用手写体识别
        include_handwriting = api_definition.get('includeHandwriting', False)
        handwriting_rules = self.handwriting_enhancement if include_handwriting else ""

        # 获取语言指令
        response_language = api_definition.get('responseLanguage', 'english')
        language_instruction = self._get_language_instruction(response_language)

        # 提取JSON结构
        json_structure = api_definition.get('jsonStructure', '')

        prompt = f"""{self.json_base_prompt}{handwriting_rules}{language_instruction}

**輸出格式：絕對嚴格**
- 你的回覆**必須是、也只能是**一個完整的 JSON 格式。
- **禁止**包含任何 `json` 程式碼區塊標籤、開頭的問候語、結尾的解釋或其他任何非 JSON 內容。
- 避免返回markdown的语法标记，特别是"```json"这样的标记
- 仅返回JSON数据，不需要任务其他说明性内容，特别是markdown的语法标记

{user_rules}
"""

        # 如果有自定义JSON结构，添加到PROMPT中
        if json_structure:
            prompt += f"""

**JSON 結構要求：**
請按照以下JSON結構返回結果：
```
{json_structure}
```"""
        else:
            # 使用默认的简单JSON结构
            prompt += """

**JSON 結構要求：**
請按照以下JSON結構返回結果,
- 如果存在表格内容，请将其转换为JSON数组的形式
```json
{
  "text": "识别到的文本内容",
  "confidence": "置信度(0-1之间的数值)",
  "fields": [
    {
      "name": "字段名称",
      "type": "field"
      "value": "字段值",
      "confidence": "该字段的置信度"
    },
    {
        "name": "表格名称",
        "type": "table",
        "rows": [
            {
                "cells": [
                    {"name": "列1名称", "value": "列1值", "confidence": "列1置信度"},
                    {"name": "列2名称", "value": "列2值", "confidence": "列2置信度"}
                ]
            },
            {
                "cells": [
                    {"name": "列1名称", "value": "列1值", "confidence": "列1置信度"},
                    {"name": "列2名称", "value": "列2值", "confidence": "列2置信度"}
                ]
            }
        ]
    }
  ]
}
```"""

        return prompt

    def generate_markdown_prompt(self, api_definition: Dict[str, Any]) -> str:
        """生成Markdown格式的PROMPT"""

        # 使用Markdown专用的基础提示词
        base_prompt = self.markdown_base_prompt

        # 检查是否启用手写体识别
        include_handwriting = api_definition.get('includeHandwriting', False)
        if include_handwriting:
            base_prompt += self.handwriting_enhancement

        # 获取语言指令
        response_language = api_definition.get('responseLanguage', 'english')
        language_instruction = self._get_language_instruction(response_language)

        # 提取用户规则
        rules = api_definition.get('rules', [])
        user_rules = self._format_user_rules(rules)

        prompt = f"""{base_prompt}{language_instruction}
**输出格式要求：**
- 你的回复必须是、也只能是完整的Markdown格式文本
- 严格遵循Markdown语法规范
- 保持原文档的结构层次和视觉布局
- 使用适当的Markdown元素（标题、表格、列表等）
- 不要添加额外的解释或说明文字

**特殊格式处理：**
- **表格**：使用标准Markdown表格语法
- **标题**：根据层级使用 #、##、### 等
- **列表**：使用 - 或 1. 表示列表项
- **强调**：重要内容使用 **粗体** 标记
- **日期**：保持原格式或转换为 yyyy-MM-dd

{user_rules}
"""

        return prompt

    def _format_user_rules(self, rules: List[str]) -> str:
        """格式化用户自定义规则"""
        if not rules:
            return ""

        formatted_rules = []
        for i, rule in enumerate(rules, 1):
            formatted_rules.append(f"{i}. {rule}")

        return f"""**用户自定义规则：**
{chr(10).join(formatted_rules)}"""

    def generate_prompt(self, api_definition: Dict[str, Any]) -> str:
        """根据API定义生成相应格式的PROMPT"""
        response_format = api_definition.get('responseFormat', 'json').lower()

        if response_format == 'markdown':
            return self.generate_markdown_prompt(api_definition)
        elif response_format == 'json':
            return self.generate_json_prompt(api_definition)
        else:
            # 默认使用JSON格式
            return self.generate_json_prompt(api_definition)


def create_ocr_prompt(api_definition: Dict[str, Any]) -> str:
    """
    便捷函数：根据API定义创建OCR PROMPT
    
    Args:
        api_definition: API定义字典，包含responseFormat、rules、jsonStructure等字段
        
    Returns:
        str: 生成的PROMPT字符串
    """
    generator = OCRPromptGenerator()
    return generator.generate_prompt(api_definition)


# 测试代码
if __name__ == "__main__":
    # 测试JSON格式
    test_api_json = {
        "apiCode": "TEST_JSON_001",
        "apiName": "测试JSON API",
        "responseFormat": "json",
        "rules": [
            "返回日期格式为 yyyy-MM-dd",
            "金额字段必须包含货币符号",
            "电话号码格式为 xxx-xxxx-xxxx"
        ]
    }

    # 测试Markdown格式
    test_api_markdown = {
        "apiCode": "TEST_MD_001",
        "apiName": "测试Markdown API",
        "responseFormat": "markdown",
        "rules": [
            "保持原始表格格式",
            "使用繁体中文",
            "日期格式统一为 yyyy年MM月dd日"
        ]
    }

    generator = OCRPromptGenerator()

    print("=== JSON格式PROMPT ===")
    print(generator.generate_prompt(test_api_json))
    print("\n" + "=" * 50 + "\n")

    print("=== Markdown格式PROMPT ===")
    print(generator.generate_prompt(test_api_markdown))
