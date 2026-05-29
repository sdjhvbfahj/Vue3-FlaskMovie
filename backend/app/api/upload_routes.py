"""
文件上传相关 API 路由
处理头像上传等功能
"""

import os
import time

from flask import request, jsonify, g, current_app
from werkzeug.utils import secure_filename

from .. import db
from ..models import User
from ..auth import login_required
from . import api_bp


def _allowed_file(filename: str) -> bool:
    """
    检查文件扩展名是否允许

    Args:
        filename: 文件名

    Returns:
        允许返回 True，否则返回 False
    """
    if "." not in filename:
        return False
    ext = filename.rsplit(".", 1)[1].lower()
    return ext in current_app.config.get("ALLOWED_EXTENSIONS", set())


@api_bp.route("/upload/avatar", methods=["POST"])
@login_required
def upload_avatar():
    """
    上传用户头像

    Request: multipart/form-data
        avatar: File     - 头像图片文件（支持 png/jpg/jpeg/gif/webp）

    Response:
        { code: 200, message: "头像上传成功", data: { avatar: "..." } }
        { code: 400, message: "错误信息" }
    """
    if "avatar" not in request.files:
        return jsonify({"code": 400, "message": "未选择文件"}), 400

    file = request.files["avatar"]
    if not file or file.filename == "":
        return jsonify({"code": 400, "message": "未选择文件"}), 400

    if not _allowed_file(file.filename):
        return jsonify({
            "code": 400,
            "message": "仅支持 png/jpg/jpeg/gif/webp 格式",
        }), 400

    # 构建安全的文件名
    username = secure_filename(g.current_username) or "user"
    ext = file.filename.rsplit(".", 1)[1].lower()
    filename = f"{username}_{int(time.time())}.{ext}"

    # 保存文件到 static/avatars/ 目录
    save_path = os.path.join(current_app.static_folder, "avatars", filename)
    os.makedirs(os.path.dirname(save_path), exist_ok=True)
    file.save(save_path)

    # 更新用户头像
    user = User.query.filter_by(username=g.current_username).first()
    if user:
        user.avatar = filename
        db.session.commit()

    return jsonify({
        "code": 200,
        "message": "头像上传成功",
        "data": {"avatar": filename},
    })
