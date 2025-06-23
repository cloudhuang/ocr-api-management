from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
import shutil
import tempfile
import os
from pathlib import Path

from src.llm_client import prepare_ollama_messages, get_ollama_response
from src.prompts import SYSTEM_PROMPT
from src.utils import process_image

# Ollama 配置
OLLAMA_MODEL = 'qwen2.5vl:32b'
OLLAMA_HOST = 'http://192.168.235.62:11434'
OLLAMA_KEY = 'KEY'
# OLLAMA_MODEL = 'qwen2.5vl:latest'
# OLLAMA_HOST = 'http://127.0.0.1:11434'

app = FastAPI()

# 添加 CORS 中间件，允许所有来源跨域访问
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 或指定前端域名列表
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/infer")
async def infer_image(file: UploadFile = File(...)):
    # 1. 保存上传的图片到临时文件
    try:
        suffix = Path(file.filename).suffix or ".png"
        with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as tmp:
            shutil.copyfileobj(file.file, tmp)
            tmp_path = tmp.name
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"图片保存失败: {e}")

    print(f"Saving image to {tmp_path}")
    # 2. 构造 task_history
    task_history = [
        ((tmp_path,), None),
        (SYSTEM_PROMPT, None),
    ]

    # 3. 消息准备与推理
    print(f"Starting prepare the LLM messages......")
    ollama_messages, error = prepare_ollama_messages(task_history, process_image)
    if error:
        os.remove(tmp_path)
        raise HTTPException(status_code=500, detail=error)

    print(f"Calling LLM for image processing......")
    response, error = get_ollama_response(ollama_messages, OLLAMA_MODEL, OLLAMA_HOST, OLLAMA_KEY)
    os.remove(tmp_path)
    if error:
        raise HTTPException(status_code=500, detail=error)

    # 4. 只返回 JSON（去除多余内容）
    try:
        import json
        result = json.loads(response)
        return JSONResponse(content=result)
    except Exception:
        return JSONResponse(content={"raw": response})

# 启动方法（命令行）：
# uvicorn src.api:app --host 0.0.0.0 --port 8000 --reload 