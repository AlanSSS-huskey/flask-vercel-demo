from fastapi import FastAPI, Request, Form
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
import uuid
import os

app = FastAPI()

# --- 路径修复 (关键) ---
# 既然调试显示路径是 /var/task/templates
# 而 /var/task 正好是 os.getcwd() (当前工作目录)
try:
    # 优先尝试 Vercel 环境的路径
    base_dir = os.getcwd()
    template_dir = os.path.join(base_dir, "templates")
    
    # 如果找不到 (比如在本地 windows 开发时)，就用相对路径兜底
    if not os.path.exists(template_dir):
        # 获取当前 api/index.py 的目录
        current_file_dir = os.path.dirname(os.path.abspath(__file__))
        # 往上跳一级找到 templates
        template_dir = os.path.join(os.path.dirname(current_file_dir), "templates")

    templates = Jinja2Templates(directory=template_dir)
except Exception as e:
    # 极端的容错：万一还不行，把错误打印出来防止 500
    print(f"Error setting up templates: {e}")
    # 这里不阻断，下面路由会报错，但在 log 里能看到

# --- 模拟数据库 ---
tasks_db = [
    {"id": "1", "title": "Deploy to Vercel", "status": "done", "tag": "Work", "date": "Today"},
    {"id": "2", "title": "Start using the App", "status": "todo", "tag": "Life", "date": "Now"},
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
