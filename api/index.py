from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse
import uuid
import os
import sys
import traceback

app = FastAPI()

# 全局变量，用于存储初始化是否成功
templates = None
init_error = None

# --- 尝试初始化模版 ---
try:
    from fastapi.templating import Jinja2Templates
    
    # 策略 1: 既然上次 Debug 说在 /var/task/templates，我们先硬编码检查这个
    path_var_task = "/var/task/templates"
    
    # 策略 2: 基于当前文件的相对路径 (api/index.py -> 上一级 -> templates)
    current_file = os.path.abspath(__file__)
    current_dir = os.path.dirname(current_file)
    parent_dir = os.path.dirname(current_dir)
    path_relative = os.path.join(parent_dir, "templates")

    # 决策逻辑
    final_path = None
    if os.path.exists(path_var_task):
        final_path = path_var_task
    elif os.path.exists(path_relative):
        final_path = path_relative
    else:
        # 如果都找不到，抛出详细错误，包含我们尝试过的路径
        raise FileNotFoundError(f"Cannot find templates. Tried: '{path_var_task}' AND '{path_relative}'. Current CWD: {os.getcwd()}")

    templates = Jinja2Templates(directory=final_path)

except Exception as e:
    # 捕获所有启动时的错误，存起来，不要让程序崩掉
    init_error = f"{str(e)}\n\nTraceback:\n{traceback.format_exc()}"

# --- 模拟数据库 ---
tasks_db = [
    {"id": "1", "title": "Deploy to Vercel", "status": "done", "tag": "Work", "date": "Today"},
    {"id": "2", "title": "Fix 500 Error", "status": "todo", "tag": "Dev", "date": "Now"},
]

# --- 路由逻辑 ---

@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    # 如果初始化失败，直接在网页上显示错误详情
    if init_error:
        return f"""
        <html>
        <body style="background:#000; color:red; font-family:monospace; padding:20px; white-space:pre-wrap;">
            <h1>⚠️ Critical Startup Error</h1>
            <hr>
            {init_error}
        </body>
        </html>
        """
    
    # 如果成功，正常渲染
    return templates.TemplateResponse("index.html", {
        "request": request, 
        "tasks": tasks_db,
    })

@app.post("/add")
async def add_task(request: Request, title: str = Form(...)):
    if init_error: return "Error"
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
    if init_error: return "Error"
    global tasks_db
    tasks_db = [t for t in tasks_db if t["id"] != task_id]
    return templates.TemplateResponse("partials/task_list.html", {
        "request": request, 
        "tasks": tasks_db
    })

@app.put("/toggle/{task_id}")
async def toggle_task(request: Request, task_id: str):
    if init_error: return "Error"
    for t in tasks_db:
        if t["id"] == task_id:
            t["status"] = "done" if t["status"] == "todo" else "todo"
    return templates.TemplateResponse("partials/task_list.html", {
        "request": request, 
        "tasks": tasks_db
    })
