import { NextRequest, NextResponse } from 'next/server';

const FLASK_API_URL = process.env.FLASK_API_URL || 'http://localhost:8000';

export async function POST(request: NextRequest) {
  try {
    const body = await request.json();
    
    // 转换前端数据格式到后端期望的格式
    // 确保 name 字段使用 apiName，这是前端表单中的字段名
    const backendData = {
      name: body.apiName, // 使用 apiName 作为主要名称字段
      description: body.description || '',
      definition: {
        // 包含所有前端发送的字段
        apiCode: body.apiCode,
        apiName: body.apiName,
        description: body.description,
        project: body.project,
        tags: body.tags || [],
        rules: body.rules || [],
        responseFormat: body.responseFormat,
        jsonStructure: body.jsonStructure,
        includeHandwriting: body.includeHandwriting || false,
        responseLanguage: body.responseLanguage || "english"
      }
    };

    console.log('Sending data to Flask backend:', JSON.stringify(backendData));

    // 调用 Flask 后端 API
    console.log(`Calling Flask API at: ${FLASK_API_URL}/api/apis`);
    
    let response;
    try {
      response = await fetch(`${FLASK_API_URL}/api/apis`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(backendData),
      });
      console.log('Response status:', response.status);
    } catch (fetchError) {
      console.error('Fetch error:', fetchError);
      return NextResponse.json(
        { error: `无法连接到后端服务器 (${FLASK_API_URL})` },
        { status: 500 }
      );
    }

    if (!response.ok) {
      let errorMessage = '保存失败';
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
      return NextResponse.json(data, { status: 201 });
    } catch (jsonError) {
      console.error('Error parsing success response:', jsonError);
      return NextResponse.json(
        { message: '操作成功，但无法解析响应' },
        { status: 201 }
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

export async function GET() {
  try {
    // 获取所有 API 定义
    console.log(`Calling Flask API at: ${FLASK_API_URL}/api/apis (GET)`);
    
    let response;
    try {
      response = await fetch(`${FLASK_API_URL}/api/apis`, {
        method: 'GET',
        headers: {
          'Content-Type': 'application/json',
        },
      });
      console.log('Response status:', response.status);
    } catch (fetchError) {
      console.error('Fetch error:', fetchError);
      return NextResponse.json(
        { error: `无法连接到后端服务器 (${FLASK_API_URL})` },
        { status: 500 }
      );
    }

    if (!response.ok) {
      let errorMessage = '获取数据失败';
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
        { message: '操作成功，但无法解析响应', data: [] },
        { status: 200 }
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