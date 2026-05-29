"""
Flask 应用工厂模块
使用应用工厂模式创建 Flask 实例，便于测试和扩展
"""

import os
import traceback
from flask import Flask, jsonify, request
from flask_cors import CORS

from .config import Config, BASE_DIR
from .extensions import db, migrate


def create_app(config_class=Config) -> Flask:
    """
    创建并配置 Flask 应用实例

    Args:
        config_class: 配置类，默认使用 Config

    Returns:
        Flask: 配置完成的 Flask 应用实例
    """
    app = Flask(
        __name__,
        static_folder=os.path.join(BASE_DIR, "static"),
        static_url_path="/static",
    )
    app.config.from_object(config_class)

    # 初始化扩展
    db.init_app(app)
    migrate.init_app(app, db)

    # 配置 CORS（跨域资源共享）
    # 显式指定允许的源和方法，并支持 credentials
    CORS(
        app,
        origins=["http://localhost:3000", "http://127.0.0.1:3000"],
        supports_credentials=True,
        methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
        allow_headers=["Content-Type", "Authorization"],
    )

    # 注册 API 蓝图（所有 API 路由统一添加 /api 前缀）
    from .api import api_bp
    app.register_blueprint(api_bp, url_prefix="/api")

    # 全局错误处理器：捕获所有未处理异常，返回 JSON 格式错误
    # 同时确保 CORS 头也会被添加到错误响应中
    @app.errorhandler(500)
    def internal_error(error):
        """处理 500 内部服务器错误"""
        # 打印完整 traceback 到控制台，方便调试
        print("\n" + "=" * 60)
        print("[500 Internal Server Error]")
        traceback.print_exc()
        print("=" * 60 + "\n")
        return jsonify({
            "code": 500,
            "message": "服务器内部错误，请检查后端控制台日志",
        }), 500

    @app.errorhandler(404)
    def not_found(error):
        """处理 404 错误"""
        return jsonify({"code": 404, "message": "接口不存在"}), 404

    @app.errorhandler(405)
    def method_not_allowed(error):
        """处理 405 方法不允许"""
        return jsonify({"code": 405, "message": "请求方法不允许"}), 405

    # after_request 钩子：确保所有响应都包含 CORS 头
    # 即使 Flask 内部抛出异常，也能保证跨域响应
    @app.after_request
    def add_cors_headers(response):
        origin = request.headers.get("Origin", "")
        # 只允许来自前端开发服务器的跨域请求
        if origin in ("http://localhost:3000", "http://127.0.0.1:3000"):
            response.headers["Access-Control-Allow-Origin"] = origin
            response.headers["Access-Control-Allow-Credentials"] = "true"
            response.headers["Access-Control-Allow-Methods"] = "GET, POST, PUT, DELETE, OPTIONS"
            response.headers["Access-Control-Allow-Headers"] = "Content-Type, Authorization"
        return response

    # 创建上传目录
    with app.app_context():
        _create_upload_folders(app)

    return app


def _create_upload_folders(app: Flask) -> None:
    """确保上传目录存在"""
    import os
    static = app.static_folder
    os.makedirs(os.path.join(static, "uploads"), exist_ok=True)
    os.makedirs(os.path.join(static, "avatars"), exist_ok=True)
    os.makedirs(os.path.join(static, "movie_pic"), exist_ok=True)
    os.makedirs(os.path.join(static, "movie_video"), exist_ok=True)
