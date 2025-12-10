from fastapi import FastAPI, Request, Form
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
import uuid
import os

app = FastAPI()

# --- 核心修复：安全地加载模板 ---
try:
    # 刚才的测试证明 Vercel 的根目录是 /var/task
    # 所以模板就在当前工作目录下的 templates 文件夹
    base_dir = os.getcwd()
    template_path = os.path.join(base_dir, "templates")
    
    # 打印路径到日志里 (Vercel 后台能看到)
    print(f"Loading templates from: {template_path}")
    
    # 初始化模板
    templates = Jinja2Templates(directory=template_path)
    
except Exception as e:
    # 如果出错，把错误存下来，稍后显示在网页上，而不是直接崩掉
    templates = None
    template_error = str(e)

# --- 模拟数据库 ---
tasks_db = [
    {"id": "1", "title": "部署成功！", "status": "done", "tag": "Milestone", "date": "Today"},
    {"id": "2", "title": "开始使用 Dashboard", "status": "todo", "tag": "Life", "date": "Now"},
]

# --- 路由 ---

@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    # 保险措施：如果模板没加载成功，直接显示错误信息
    if templates is None:
        return f"""
        <html><body>
            <h1>Startup Error</h1>
            <p>Could not load templates folder.</p>
            <p>Error details: {template_error}</p>
            <p>Current Directory: {os.getcwd()}</p>
        </body></html>
        """
        
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
