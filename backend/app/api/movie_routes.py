"""
电影相关 API 路由
处理电影的查询、搜索、分类筛选等操作
"""

from flask import request, jsonify
from sqlalchemy import or_

from .. import db
from ..models import Movie, Collect
from ..auth import login_required
from . import api_bp


@api_bp.route("/movies", methods=["GET"])
@login_required
def get_movies():
    """
    获取电影列表（支持分页、分类筛选、关键词搜索）

    Query Parameters:
        page: int        - 页码（默认 1）
        per_page: int    - 每页数量（默认 28）
        category: str    - 分类筛选（可选，"" 或 "全部" 表示不筛选）
        keyword: str     - 搜索关键词（可选）

    Response:
        { code: 200, data: { movies: [...], pagination: { ... }, categories: [...] } }
    """
    page = request.args.get("page", 1, type=int)
    per_page = request.args.get("per_page", 28, type=int)
    category = (request.args.get("category", "") or "").strip()
    keyword = (request.args.get("keyword", "") or "").strip()

    # 获取所有分类列表
    categories_rows = db.session.query(Movie.category).distinct().all()
    categories = sorted([c[0] for c in categories_rows if c[0]])

    # 构建查询
    query = Movie.query

    # 分类筛选
    if category and category != "全部":
        query = query.filter(Movie.category == category)

    # 关键词搜索（搜索标题和简介）
    if keyword:
        query = query.filter(
            or_(
                Movie.title.like(f"%{keyword}%"),
                Movie.info.like(f"%{keyword}%"),
            )
        )

    # 按热度排序
    query = query.order_by(Movie.likes.desc(), Movie.id.desc())

    # 分页
    pagination = query.paginate(page=page, per_page=per_page, error_out=False)

    return jsonify({
        "code": 200,
        "data": {
            "movies": [m.to_dict() for m in pagination.items],
            "pagination": {
                "page": pagination.page,
                "per_page": pagination.per_page,
                "total": pagination.total,
                "pages": pagination.pages,
                "has_prev": pagination.has_prev,
                "has_next": pagination.has_next,
                "prev_num": pagination.prev_num,
                "next_num": pagination.next_num,
            },
            "categories": categories,
        },
    })


@api_bp.route("/movies/banners", methods=["GET"])
def get_banners():
    """
    获取首页 Banner 电影列表

    返回所有 is_banner=1 的电影，按 banner_order 升序排列

    Response:
        { code: 200, data: { banners: [...] } }
    """
    banners = (
        Movie.query
        .filter(Movie.is_banner == 1)
        .order_by(Movie.banner_order.asc())
        .all()
    )

    return jsonify({
        "code": 200,
        "data": {
            "banners": [b.to_dict() for b in banners],
        },
    })


@api_bp.route("/movies/home", methods=["GET"])
@login_required
def get_home_movies():
    """
    获取首页各分类的电影数据

    返回按分类分组的电影列表，每个分类最多 20 部

    Response:
        { code: 200, data: { categories: [...], movies_by_category: { "全部": [...], ... } } }
    """
    # 获取所有分类
    categories_rows = db.session.query(Movie.category).distinct().all()
    categories = sorted([c[0] for c in categories_rows if c[0]])
    categories.insert(0, "全部")

    # 按分类获取电影
    movies_by_category = {}

    # "全部" 分类：按热度排序，获取所有电影
    movies_by_category["全部"] = [
        m.to_dict()
        for m in Movie.query.order_by(Movie.likes.desc()).limit(20).all()
    ]

    # 各分类
    for cat in categories:
        if cat == "全部":
            continue
        movies_by_category[cat] = [
            m.to_dict()
            for m in (
                Movie.query
                .filter(Movie.category == cat)
                .order_by(Movie.likes.desc())
                .limit(20)
                .all()
            )
        ]

    return jsonify({
        "code": 200,
        "data": {
            "categories": categories,
            "movies_by_category": movies_by_category,
        },
    })


@api_bp.route("/movies/<int:movie_id>", methods=["GET"])
@login_required
def get_movie_detail(movie_id: int):
    """
    获取电影详情

    Path Parameters:
        movie_id: int   - 电影 ID

    Response:
        { code: 200, data: { movie: { ... }, is_collected: bool } }
    """
    from flask import g

    movie = Movie.query.get(movie_id)
    if not movie:
        return jsonify({"code": 404, "message": "电影不存在"}), 404

    # 检查当前用户是否已收藏
    is_collected = False
    username = g.current_username if hasattr(g, "current_username") else None
    if username:
        collect = Collect.query.filter_by(
            user=username, movie_id=movie_id
        ).first()
        is_collected = collect is not None

    # 获取同类推荐（同分类，按热度排序，排除当前电影，最多 8 部）
    recommends = []
    if movie.category:
        recommend_movies = (
            Movie.query
            .filter(
                Movie.category == movie.category,
                Movie.id != movie.id,
            )
            .order_by(Movie.likes.desc())
            .limit(8)
            .all()
        )
        recommends = [m.to_dict() for m in recommend_movies]

    return jsonify({
        "code": 200,
        "data": {
            "movie": movie.to_dict(),
            "is_collected": is_collected,
            "recommends": recommends,
        },
    })
