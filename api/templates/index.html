from flask import Flask, render_template
import os

# --- 1. 路径设置 (确保Vercel能找到文件) ---
base_dir = os.path.dirname(os.path.abspath(__file__))
template_dir = os.path.join(base_dir, 'templates')
app = Flask(__name__, template_folder=template_dir)

# --- 2. 核心逻辑 ---
@app.route('/')
def dashboard_home():
    # === 准备假数据区域 (以后这里换成读数据库的代码) ===
    # 我们创建一个字典(dictionary)，把想显示的数据都放进去
    fake_data = {
        # 顶部卡片的数字
        "total_users": 1205,
        "monthly_income": "¥ 84,000",
        "pending_tasks": 3,
        # 表格里的数据列表
        "recent_orders": [
            {"id": "#1001", "user": "张三", "date": "2023-10-20", "amount": "¥120", "status": "已完成"},
            {"id": "#1002", "user": "李四", "date": "2023-10-21", "amount": "¥350", "status": "处理中"},
            {"id": "#1003", "user": "王五", "date": "2023-10-21", "amount": "¥80",  "status": "已完成"},
            {"id": "#1004", "user": "赵六", "date": "2023-10-22", "amount": "¥900", "status": "已取消"},
            {"id": "#1005", "user": "钱七", "date": "2023-10-22", "amount": "¥150", "status": "已完成"},
        ]
    }
    
    # 把准备好的 fake_data 传给网页 template
    return render_template('index.html', data=fake_data)

# Vercel 必须项
app = app
