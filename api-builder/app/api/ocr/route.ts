import { NextRequest, NextResponse } from 'next/server';

const FLASK_API_URL = process.env.FLASK_API_URL || 'http://localhost:8000';

export async function POST(request: NextRequest) {
  try {
    // 从请求中获取表单数据
    const formData = await request.formData();
    
    console.log('Forwarding OCR request to Flask backend');
    
    // 将请求转发到 Flask 后端
    const response = await fetch(`${FLASK_API_URL}/api/ocr`, {
      method: 'POST',
      body: formData,
    });
    
    if (!response.ok) {
      let errorMessage = 'OCR 处理失败';
      try {
        const errorData = await response.text();
        console.error('Flask API error response:', errorData);
        
        // 尝试解析为 JSON
        try {
          const jsonError = JSON.parse(errorData);
          errorMessage = jsonError.error || errorMessage;
        } catch (jsonError) {
          // 如果不是有效的 JSON，使用文本响应
          errorMessage = errorData || errorMessage;
        }
      } catch (textError) {
        console.error('Error reading response text:', textError);
      }
      
      return NextResponse.json(
        { error: errorMessage },
        { status: response.status }
      );
    }
    
    try {
      const data = await response.json();
      return NextResponse.json(data);
    } catch (jsonError) {
      console.error('Error parsing success response:', jsonError);
      return NextResponse.json(
        { error: '无法解析响应数据' },
        { status: 500 }
      );
    }
  } catch (error) {
    console.error('API Error:', error);
    return NextResponse.json(
      { error: '服务器错误' },
      { status: 500 }
    );
  }
}