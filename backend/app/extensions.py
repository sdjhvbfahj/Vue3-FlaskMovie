"""
Flask 扩展初始化模块
在此统一初始化所有 Flask 扩展，避免循环导入问题
"""

from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

# 数据库 ORM 实例
db = SQLAlchemy()

# 数据库迁移实例
migrate = Migrate()
