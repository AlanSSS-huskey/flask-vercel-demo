from fastapi import FastAPI
from fastapi.responses import HTMLResponse, JSONResponse
import os

app = FastAPI()

@app.get("/", response_class=HTMLResponse)
async def read_root():
    # 1. 获取当前工作目录
    cwd = os.getcwd()
    
    # 2. 获取当前文件(api/index.py)的目录
    file_dir = os.path.dirname(os.path.abspath(__file__))
    
    # 3. 尝试查找 templates 文件夹
    # 方案 A: 在当前工作目录下找
    path_a = os.path.join(cwd, "templates")
    exists_a = os.path.exists(path_a)
    
    # 方案 B: 在 api 文件夹的上一级找
    path_b = os.path.join(os.path.dirname(file_dir), "templates")
    exists_b = os.path.exists(path_b)
    
    # 4. 列出当前目录下的所有文件（看看文件到底在哪）
    try:
        files_in_cwd = os.listdir(cwd)
    except:
        files_in_cwd = "Error listing files"

    # --- 如果两个都找不到，显示诊断信息 ---
    if not exists_a and not exists_b:
        return f"""
        <html>
        <body style="font-family: monospace; background: #222; color: #fff; padding: 20px;">
            <h1 style="color: red;">Still looking for templates...</h1>
            <p><strong>Current Working Directory (CWD):</strong> {cwd}</p>
            <p><strong>Files in CWD:</strong> {files_in_cwd}</p>
            <hr>
            <p><strong>Path A (Attempt):</strong> {path_a} -> Exists? {exists_a}</p>
            <p><strong>Path B (Attempt):</strong> {path_b} -> Exists? {exists_b}</p>
        </body>
        </html>
        """

    # --- 如果找到了，尝试加载 ---
    # 优先使用存在的那个路径
    valid_path = path_a if exists_a else path_b
    
    try:
        from fastapi.templating import Jinja2Templates
        templates = Jinja2Templates(directory=valid_path)
        # 这里为了测试，我们手动渲染一下，不依赖 request
        # 正常代码应该用 TemplateResponse
        return f"""
        <html>
        <body style="font-family: sans-serif; background: #000; color: #0f0; padding: 20px; text-align: center;">
            <h1>✅ Success! Found templates at:</h1>
            <code style="background: #333; padding: 5px;">{valid_path}</code>
            <p>Now I know the correct path. You can restore the real code using this path.</p>
        </body>
        </html>
        """
    except Exception as e:
        return f"Error loading Jinja2: {str(e)}"

# 为了防止 Vercel 找不到路由，加个简单的 ping
@app.get("/ping")
def ping():
    return {"status": "alive"}
