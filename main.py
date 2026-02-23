from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
import requests
import os

app = FastAPI()
templates = Jinja2Templates(directory="templates")

# 从环境变量读取 API Key
OPENAI_KEY = os.getenv("OPENAI_API_KEY")

@app.get("/", response_class=HTMLResponse)
def home(request: Request):
    # 返回前端网页
    return templates.TemplateResponse("index.html", {"request": request})

@app.post("/chat")
def chat(model: str = Form(...), message: str = Form(...)):
    """
    聊天接口，根据选择模型调用 OpenAI API
    """
    headers = {
        "Authorization": f"Bearer {OPENAI_KEY}",
        "Content-Type": "application/json"
    }
    data = {
        "model": model,
        "messages": [{"role":"user","content": message}]
    }

    try:
        r = requests.post("https://api.openai.com/v1/chat/completions", headers=headers, json=data)
        res = r.json()
        return {"reply": res["choices"][0]["message"]["content"]}
    except Exception as e:
        return {"reply": f"调用失败: {str(e)}"}

@app.post("/image")
def generate_image(prompt: str = Form(...)):
    """
    图片生成接口
    """
    headers = {
        "Authorization": f"Bearer {OPENAI_KEY}",
        "Content-Type": "application/json"
    }
    data = {
        "model": "gpt-image-1",
        "prompt": prompt,
        "n": 1,
        "size": "512x512"
    }

    try:
        r = requests.post("https://api.openai.com/v1/images/generations", headers=headers, json=data)
        res = r.json()
        return {"url": res["data"][0]["url"]}
    except Exception as e:
        return {"url": "", "error": str(e)}
