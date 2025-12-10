from flask import Flask

app = Flask(__name__)

@app.route('/')
def home():
    return """
    <!DOCTYPE html>
    <html lang="zh-CN">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>我的 Vercel 网站</title>
        <style>
            body {
                font-family: system-ui, -apple-system, sans-serif;
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                height: 100vh;
                margin: 0;
                display: flex;
                justify-content: center;
                align-items: center;
                color: white;
            }
            .card {
                background: rgba(255, 255, 255, 0.2);
                backdrop-filter: blur(10px);
                padding: 40px;
                border-radius: 20px;
                text-align: center;
                box-shadow: 0 4px 30px rgba(0, 0, 0, 0.1);
                border: 1px solid rgba(255, 255, 255, 0.3);
            }
            h1 { margin: 0 0 10px 0; }
        </style>
    </head>
    <body>
        <div class="card">
            <h1>🎉 救活了！</h1>
            <p>不需要读取外部文件，这样最稳。</p>
            <p>Status: <b>Online</b></p>
        </div>
    </body>
    </html>
    """

# 这一行必须保留
app = app
