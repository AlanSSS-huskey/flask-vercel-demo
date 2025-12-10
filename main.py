# main.py
from fastapi import FastAPI, Request, Form
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from typing import List, Optional
import uuid
from datetime import datetime

app = FastAPI()

# 配置模板文件夹
# main.py 修改前:
# templates = Jinja2Templates(directory="templates")

# main.py 修改后 (请替换):
import os
from fastapi import FastAPI, Request, Form
from fastapi.templating import Jinja2Templates
# ... 其他 import ...

app = FastAPI()

# 获取 main.py 所在的绝对路径
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
# 拼接出 templates 的绝对路径
TEMPLATE_DIR = os.path.join(BASE_DIR, "templates")

# 使用绝对路径
templates = Jinja2Templates(directory=TEMPLATE_DIR)

# ... 下面是原本的路由代码 ...

# --- 模拟数据库 (内存版) ---
# 注意：在 Vercel Serverless 上，全局变量会在一段时间后重置。
# 真正上线需要连接外部数据库 (如 Vercel KV, Supabase, Neon)。
# 这里为了演示方便，先用内存列表。
class Task(BaseModel):
    id: str
    title: str
    status: str = "todo" # todo, done
    tag: str = "Inbox"
    date: str

tasks_db = [
    {"id": "1", "title": "设计 Dashboard 原型", "status": "done", "tag": "Work", "date": "Today"},
    {"id": "2", "title": "学习 FastAPI", "status": "todo", "tag": "Study", "date": "Tomorrow"},
]

# --- 路由逻辑 ---

@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    return templates.TemplateResponse("index.html", {
        "request": request, 
        "tasks": tasks_db,
        "count": len(tasks_db)
    })

# 添加任务 (HTMX 触发)
@app.post("/add")
async def add_task(request: Request, title: str = Form(...)):
    new_task = {
        "id": str(uuid.uuid4()),
        "title": title,
        "status": "todo",
        "tag": "Inbox",
        "date": "Today"
    }
    tasks_db.insert(0, new_task) # 插入到最前面
    
    # 只返回任务列表片段，而不是整个页面 (HTMX 的魔法)
    return templates.TemplateResponse("partials/task_list.html", {
        "request": request, 
        "tasks": tasks_db
    })

# 删除任务
@app.delete("/delete/{task_id}")
async def delete_task(request: Request, task_id: str):
    global tasks_db
    tasks_db = [t for t in tasks_db if t["id"] != task_id]
    return templates.TemplateResponse("partials/task_list.html", {
        "request": request, 
        "tasks": tasks_db
    })

# 切换状态
@app.put("/toggle/{task_id}")
async def toggle_task(request: Request, task_id: str):
    for t in tasks_db:
        if t["id"] == task_id:
            t["status"] = "done" if t["status"] == "todo" else "todo"
    return templates.TemplateResponse("partials/task_list.html", {
        "request": request, 
        "tasks": tasks_db
    })
