"""
数据库初始化脚本
用于创建所有数据库表，并可选地创建管理员账号

使用方式：
    python init_db.py
"""

import sys
import io

# 修复 Windows 控制台编码问题（GBK 无法输出 emoji）
if sys.platform == "win32":
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")

from app import create_app
from app.extensions import db
from app.models import User
from app.auth import hash_password

app = create_app()

with app.app_context():
    # 创建所有表
    db.create_all()
    print("[OK] 数据库表创建完成")

    # 检查是否已存在管理员账号，如果没有则创建
    admin = User.query.filter_by(username="admin").first()
    if not admin:
        admin = User(
            username="admin",
            password=hash_password("admin123"),
            bio="系统管理员",
            is_banned=0,
        )
        db.session.add(admin)
        db.session.commit()
        print("[OK] 管理员账号创建成功（用户名: admin, 密码: admin123）")
    else:
        print("[INFO] 管理员账号已存在，跳过创建")
