import { NextRequest, NextResponse } from 'next/server';

const FLASK_API_URL = process.env.FLASK_API_URL || 'http://localhost:8000';

export async function GET(
  request: NextRequest,
  { params }: { params: { id: string } }
) {
  const id = params.id;
  
  try {
    console.log(`Fetching API with ID: ${id}`);
    
    // 调用 Flask 后端 API
    const response = await fetch(`${FLASK_API_URL}/api/apis/${id}`, {
      method: 'GET',
      headers: {
        'Content-Type': 'application/json',
      },
    });
    
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

export async function PUT(
  request: NextRequest,
  { params }: { params: { id: string } }
) {
  const id = params.id;
  
  try {
    const body = await request.json();
    
    // 转换前端数据格式到后端期望的格式
    const backendData = {
      name: body.apiName,
      description: body.description || '',
      definition: {
        apiCode: body.apiCode,
        apiName: body.apiName,
        description: body.description,
        project: body.project,
        tags: body.tags || [],
        rules: body.rules || [],
        responseFormat: body.responseFormat,
        jsonStructure: body.jsonStructure
      }
    };
    
    console.log(`Updating API with ID: ${id}`);
    console.log('Sending data to Flask backend:', JSON.stringify(backendData));
    
    // 调用 Flask 后端 API
    const response = await fetch(`${FLASK_API_URL}/api/apis/${id}`, {
      method: 'PUT',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(backendData),
    });
    
    if (!response.ok) {
      let errorMessage = '更新失败';
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
      return NextResponse.json(data, { status: 200 });
    } catch (jsonError) {
      console.error('Error parsing success response:', jsonError);
      return NextResponse.json(
        { message: '操作成功，但无法解析响应' },
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

export async function DELETE(
  request: NextRequest,
  { params }: { params: { id: string } }
) {
  const id = params.id;
  
  try {
    console.log(`Deleting API with ID: ${id}`);
    
    // 调用 Flask 后端 API
    const response = await fetch(`${FLASK_API_URL}/api/apis/${id}`, {
      method: 'DELETE',
    });
    
    if (!response.ok) {
      let errorMessage = '删除失败';
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
    
    return NextResponse.json({ success: true }, { status: 200 });
  } catch (error) {
    console.error('API Error:', error);
    return NextResponse.json(
      { error: '服务器错误' },
      { status: 500 }
    );
  }
}