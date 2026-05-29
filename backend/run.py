"""
Flask 应用入口文件
用于启动后端 API 服务

启动方式：
    python run.py

或使用 gunicorn（生产环境）：
    gunicorn -w 4 -b 0.0.0.0:5000 run:app
"""

import os

from app import create_app

# 创建 Flask 应用实例
app = create_app()

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    debug = os.environ.get("FLASK_DEBUG", "True").lower() == "true"
    app.run(host="0.0.0.0", port=port, debug=debug)
