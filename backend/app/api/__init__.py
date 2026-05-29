"""
API 蓝图初始化
将所有 API 子模块集中注册
"""

from flask import Blueprint

# 创建 API 蓝图
api_bp = Blueprint("api", __name__)

# 导入各个子路由模块（在蓝图创建之后导入，避免循环导入）
from . import auth_routes      # noqa: E402, F401
from . import movie_routes     # noqa: E402, F401
from . import comment_routes   # noqa: E402, F401
from . import collect_routes   # noqa: E402, F401
from . import user_routes      # noqa: E402, F401
from . import upload_routes    # noqa: E402, F401
from . import admin_routes     # noqa: E402, F401
