"""
收藏相关 API 路由
处理电影的收藏/取消收藏操作，查看收藏列表
"""

from flask import request, jsonify, g

from .. import db
from ..models import Movie, Collect
from ..auth import login_required
from . import api_bp


@api_bp.route("/collects/toggle/<int:movie_id>", methods=["POST"])
@login_required
def toggle_collect(movie_id: int):
    """
    切换收藏状态（收藏 / 取消收藏）

    如果已经收藏则取消收藏（likes - 1），反之则添加收藏（likes + 1）

    Path Parameters:
        movie_id: int   - 电影 ID

    Response:
        { code: 200, message: "...", data: { is_collected: bool, likes: int } }
    """
    movie = Movie.query.get(movie_id)
    if not movie:
        return jsonify({"code": 404, "message": "电影不存在"}), 404

    username = g.current_username

    # 查找是否已收藏
    collect = Collect.query.filter_by(
        user=username,
        movie_id=movie_id,
    ).first()

    if collect:
        # 取消收藏
        db.session.delete(collect)
        if movie.likes > 0:
            movie.likes -= 1
        db.session.commit()
        return jsonify({
            "code": 200,
            "message": "已取消收藏",
            "data": {"is_collected": False, "likes": movie.likes},
        })
    else:
        # 添加收藏
        db.session.add(Collect(user=username, movie_id=movie_id))
        movie.likes += 1
        db.session.commit()
        return jsonify({
            "code": 200,
            "message": "收藏成功",
            "data": {"is_collected": True, "likes": movie.likes},
        })


@api_bp.route("/collects", methods=["GET"])
@login_required
def get_collects():
    """
    获取当前用户的收藏列表（支持分页和分类筛选）

    Query Parameters:
        page: int        - 页码（默认 1）
        per_page: int    - 每页数量（默认 24）
        category: str    - 分类筛选（可选）

    Response:
        { code: 200, data: { collects: [...], pagination: { ... }, categories: [...] } }
    """
    page = request.args.get("page", 1, type=int)
    per_page = request.args.get("per_page", 24, type=int)
    category = (request.args.get("category", "") or "").strip()

    username = g.current_username

    # 获取用户收藏的所有分类
    category_rows = (
        db.session.query(Movie.category)
        .join(Collect, Collect.movie_id == Movie.id)
        .filter(Collect.user == username)
        .distinct()
        .all()
    )
    categories = sorted([c[0] for c in category_rows if c[0]])

    # 构建查询：收藏的电影
    query = (
        Movie.query
        .join(Collect, Collect.movie_id == Movie.id)
        .filter(Collect.user == username)
    )

    # 分类筛选
    if category and category != "全部":
        query = query.filter(Movie.category == category)

    # 按收藏时间倒序
    query = query.order_by(Collect.id.desc())

    # 分页
    pagination = query.paginate(page=page, per_page=per_page, error_out=False)

    # 构建收藏数据（包含电影信息）
    collects_data = []
    for movie in pagination.items:
        collects_data.append({
            "id": movie.id,
            "title": movie.title,
            "poster": movie.poster or "",
            "category": movie.category or "",
            "likes": movie.likes,
        })

    return jsonify({
        "code": 200,
        "data": {
            "collects": collects_data,
            "pagination": {
                "page": pagination.page,
                "per_page": pagination.per_page,
                "total": pagination.total,
                "pages": pagination.pages,
                "has_prev": pagination.has_prev,
                "has_next": pagination.has_next,
            },
            "categories": categories,
        },
    })


@api_bp.route("/collects/<int:collect_id>", methods=["DELETE"])
@login_required
def delete_collect(collect_id: int):
    """
    通过收藏 ID 删除收藏记录

    Path Parameters:
        collect_id: int - 收藏记录 ID

    Response:
        { code: 200, message: "已取消收藏" }
    """
    collect = Collect.query.get(collect_id)

    if not collect:
        return jsonify({"code": 404, "message": "收藏记录不存在"}), 404

    if collect.user != g.current_username:
        return jsonify({"code": 403, "message": "无权限操作"}), 403

    # 更新电影热度
    movie = Movie.query.get(collect.movie_id)
    if movie and movie.likes > 0:
        movie.likes -= 1

    db.session.delete(collect)
    db.session.commit()

    return jsonify({"code": 200, "message": "已取消收藏"})
