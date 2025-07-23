"""
OCR PROMPT 生成器
根据API定义动态生成不同格式的PROMPT
"""
import json
from typing import Dict, List, Any


class OCRPromptGenerator:
    """OCR PROMPT 生成器类"""
    
    def __init__(self):
        self.base_system_prompt = """你是一個高精度的 AI 表單辨識服務。你的唯一任務是分析在此次請求中提供的圖片，並根據下方的要求，返回识别的结果。

**核心指令：**
分析提供的圖片，识别图片中的内容。你的所有輸出都必須基於圖片中的視覺證據。

**辨識準確性與置信度規則 (Accuracy and Confidence Rules)：**
1. **高置信度原則**：只有在您對辨識結果有高置信度時，才輸出文字內容。
2. **無法辨識處理**：如果某個欄位有手寫痕跡，但因字跡潦草或影像模糊而**無法準確辨識**，請在該欄位的 `value` 中返回特定字串 `"[UNRECOGNIZABLE]"`。
3. **嚴禁猜測**：**嚴禁猜測**或捏造內容。不確定即等於無法辨識。準確性是最高優先級。
4. **空白欄位處理**：如果某個欄位**完全空白**，沒有任何手寫痕跡，其 `value` 應為**空字串 `""`**。這與「無法辨識」是兩種不同的情況。
5. **簽名處理**：對於簽名欄位 (如「申請人/受益人簽名」)，由於其高度個人化且通常難以辨識為標準文字，請一律在 `value` 中返回 `"[SIGNATURE]"`，除非簽名為非常清晰的正楷。"""

    def generate_json_prompt(self, api_definition: Dict[str, Any]) -> str:
        """生成JSON格式的PROMPT"""
        
        # 提取用户规则
        rules = api_definition.get('rules', [])
        user_rules = self._format_user_rules(rules)
        
        # 提取JSON结构
        json_structure = api_definition.get('jsonStructure', '')
        
        prompt = f"""{self.base_system_prompt}

{user_rules}

**輸出格式：絕對嚴格**
- 你的回覆**必須是、也只能是**一個完整的 JSON 格式。
- **禁止**包含任何 `json` 程式碼區塊標籤、開頭的問候語、結尾的解釋或其他任何非 JSON 內容。
- 避免返回markdown的语法标记，特别是"```json"这样的标记
- 仅返回JSON数据，不需要任务其他说明性内容，特别是markdown的语法标记
- 对于打钩类回复，比如：團體險 (已勾選)， 返回 團體險 作为value
- 对于有编号的回复，比如 "5 豁免保費"，是返回内容： "豁免保費", 不需要返回编号
- 使用繁体中文回复
- 返回日期格式为 **yyyy-MM-dd**"""

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
請按照以下JSON結構返回結果：
```json
{
  "text": "识别到的文本内容",
  "confidence": "置信度(0-1之间的数值)",
  "fields": [
    {
      "name": "字段名称",
      "value": "字段值",
      "confidence": "该字段的置信度"
    }
  ]
}
```"""

        return prompt

    def generate_markdown_prompt(self, api_definition: Dict[str, Any]) -> str:
        """生成Markdown格式的PROMPT"""
        
        # 提取用户规则
        rules = api_definition.get('rules', [])
        user_rules = self._format_user_rules(rules)
        
        prompt = f"""{self.base_system_prompt}

{user_rules}

**輸出格式：絕對嚴格**
- 你的回覆**必須是、也只能是**一個完整的Markdown的文本。
- 图片识别的文本内容，通过markdown的语法返回
- 如果识别出来的是文本，你需要严格遵行文本的格式。
- 如果识别出来的是表格，你需要严格遵行原表格的格式。
- 如果识别出来的表格内容，直接返回markdown格式的表格,格式参考{{Markdown表格参考}}
- 严格遵循Markdown语法，确保格式正确。
- 使用繁体中文回复

## Markdown表格参考
| 欄位名稱 | 內容 |
| -------- | ------- |
| 姓名 | 張三 |
| 日期 | 2024-01-01 |
| 金額 | $1,000 |"""

        return prompt

    def _format_user_rules(self, rules: List[str]) -> str:
        """格式化用户自定义规则"""
        if not rules:
            return ""
        
        formatted_rules = []
        for i, rule in enumerate(rules, 1):
            formatted_rules.append(f"{i}. {rule}")
        
        return f"""
**用戶自定義規則：**
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
        ],
        "jsonStructure": '{"name": "string", "date": "string", "amount": "string", "phone": "string"}'
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
    print("\n" + "="*50 + "\n")
    
    print("=== Markdown格式PROMPT ===")
    print(generator.generate_prompt(test_api_markdown))
