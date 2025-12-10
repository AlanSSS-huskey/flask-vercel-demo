# api/index.py
import sys
import os

# 获取当前文件的目录 (即 api/)
current_dir = os.path.dirname(os.path.abspath(__file__))
# 获取父目录 (即根目录)
parent_dir = os.path.dirname(current_dir)

# 将根目录加入到系统路径，这样才能 import main
sys.path.append(parent_dir)

from main import app

# Vercel 需要这个
if __name__ == "__main__":
    app.run()
