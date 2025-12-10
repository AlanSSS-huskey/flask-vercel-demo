from fastapi import FastAPI, Request, Form
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
import uuid
import os

app = FastAPI()

# --- 路径查找逻辑 (适配 Vercel) ---
def get_template_dir():
    # 1. 获取当前文件 (api/index.py) 的绝对路径
    current_file_path = os.path.abspath(__file__)
    
    # 2. 获取当前文件所在目录 (api/)
    current_dir = os.path.dirname(current_file_path)
    
    # 3. 获取项目根目录 (api/ 的上一级)
    project_root = os.path.dirname(current_dir)
    
    # 4. 拼接 templates 路径
    template_path = os.path.join(project_root, "templates")
    
    return template_path

# 初始化模板
template_dir = get_template_dir()
templates = Jinja2Templates(directory=template_dir)

# --- 模拟数据库 ---
tasks_db = [
    {"id": "1", "title": "Config vercel.json", "status": "done", "tag": "Fix", "date": "Today"},
    {"id": "2", "title": "Read HTML files correctly", "status": "todo", "tag": "Dev", "date": "Now"},
]

# --- 路由逻辑 ---

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
