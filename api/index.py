from flask import Flask, render_template
import os

# 获取当前这个 index.py 文件所在的绝对路径
base_dir = os.path.dirname(os.path.abspath(__file__))
# 拼接出 templates 的路径
template_dir = os.path.join(base_dir, 'templates')

# 明确告诉 Flask：模板就在我隔壁的 templates 文件夹里
app = Flask(__name__, template_folder=template_dir)

@app.route('/')
def home():
    return render_template('index.html')

# 必须有这一行
app = app
