# api/index.py
from fastapi import FastAPI, Request, Form
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
import uuid
import os

# --- 1. 初始化 App ---
app = FastAPI()

# --- 2. 修复模版路径 (关键点) ---
# Vercel 的文件结构中，api/index.py 在 api 文件夹里
# 而 templates 文件夹在根目录 (即 api 的上一级)
current_dir = os.path.dirname(os.path.abspath(__file__))
# 往上跳一级，找到 templates
template_dir = os.path.join(os.path.dirname(current_dir), "templates")

# 容错处理：打印路径到日志，万一报错方便看
print(f"Loading templates from: {template_dir}")

templates = Jinja2Templates(directory=template_dir)

# --- 3. 模拟数据库 ---
tasks_db = [
    {"id": "1", "title": "Deploy to Vercel", "status": "done", "tag": "Work", "date": "Today"},
    {"id": "2", "title": "Fix 500 Error", "status": "todo", "tag": "Dev", "date": "Now"},
]

# --- 4. 路由逻辑 ---

@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    return templates.TemplateResponse("index.html", {
        "request": request, 
        "tasks": tasks_db,
    })

@app.post("/add")
async def add_task(request: Request, title: str = Form(...)):
    new_task = {
        "id": str(uuid.uuid4()),
        "title": title,
        "status": "todo",
        "tag": "Inbox",
        "date": "Today"
    }
    tasks_db.insert(0, new_task)
    return templates.TemplateResponse("partials/task_list.html", {
        "request": request, 
        "tasks": tasks_db
    })

@app.delete("/delete/{task_id}")
async def delete_task(request: Request, task_id: str):
    global tasks_db
    tasks_db = [t for t in tasks_db if t["id"] != task_id]
    return templates.TemplateResponse("partials/task_list.html", {
        "request": request, 
        "tasks": tasks_db
    })

@app.put("/toggle/{task_id}")
async def toggle_task(request: Request, task_id: str):
    for t in tasks_db:
        if t["id"] == task_id:
            t["status"] = "done" if t["status"] == "todo" else "todo"
    return templates.TemplateResponse("partials/task_list.html", {
        "request": request, 
        "tasks": tasks_db
    })
