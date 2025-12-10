from flask import Flask, render_template, request, redirect, url_for
import os

# --- 1. 基础配置 ---
base_dir = os.path.dirname(os.path.abspath(__file__))
template_dir = os.path.join(base_dir, 'templates')
app = Flask(__name__, template_folder=template_dir)

# --- 2. 临时数据库 (用一个列表代替) ---
# 格式: {'id': 1, 'content': '买牛奶', 'done': False}
todos = [
    {'id': 1, 'content': '部署网站到 Vercel', 'done': True},
    {'id': 2, 'content': '学习 Python Flask', 'done': False}
]
next_id = 3

# --- 3. 路由逻辑 ---

# 首页：展示清单
@app.route('/')
def index():
    return render_template('index.html', todos=todos)

# 添加任务
@app.route('/add', methods=['POST'])
def add():
    global next_id
    content = request.form.get('content')
    if content:
        todos.append({'id': next_id, 'content': content, 'done': False})
        next_id += 1
    return redirect(url_for('index'))

# 删除任务
@app.route('/delete/<int:todo_id>')
def delete(todo_id):
    global todos
    # 重新过滤列表，把 id 匹配的删掉
    todos = [t for t in todos if t['id'] != todo_id]
    return redirect(url_for('index'))

# 标记完成/未完成
@app.route('/toggle/<int:todo_id>')
def toggle(todo_id):
    for t in todos:
        if t['id'] == todo_id:
            t['done'] = not t['done']
    return redirect(url_for('index'))

# Vercel 需要这一行
app = app
