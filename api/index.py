from flask import Flask, render_template

# 指向上一级的 templates 目录
app = Flask(__name__, template_folder='../templates')

@app.route('/')
def home():
    # 这里可以写你的后端逻辑，比如读取数据库等
    # 现在我们直接返回网页
    return render_template('index.html')

# Vercel 需要这一行
app = app
