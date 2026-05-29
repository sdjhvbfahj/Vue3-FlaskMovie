"""
管理后台相关 API 路由
仅限管理员（username == "admin"）访问
处理用户管理、电影管理、评论管理等操作
"""

import os

from flask import request, jsonify
from werkzeug.utils import secure_filename

from .. import db
from ..models import User, Movie, Comment
from ..auth import admin_required
from . import api_bp


# ================== 后台统计 ==================

@api_bp.route("/admin/stats", methods=["GET"])
@admin_required
def admin_stats():
    """
    获取后台统计数据

    Response:
        { code: 200, data: { user_count, movie_count, comment_count } }
    """
    return jsonify({
        "code": 200,
        "data": {
            "user_count": User.query.count(),
            "movie_count": Movie.query.count(),
            "comment_count": Comment.query.count(),
        },
    })


# ================== 用户管理 ==================

@api_bp.route("/admin/users", methods=["GET"])
@admin_required
def admin_users():
    """
    获取所有用户列表

    Response:
        { code: 200, data: { users: [...] } }
    """
    users = User.query.order_by(User.id.asc()).all()
    return jsonify({
        "code": 200,
        "data": {
            "users": [u.to_dict() for u in users],
        },
    })


@api_bp.route("/admin/users/<int:user_id>/toggle_ban", methods=["POST"])
@admin_required
def admin_toggle_ban(user_id: int):
    """
    封禁 / 解封用户

    Path Parameters:
        user_id: int    - 用户 ID

    Response:
        { code: 200, message: "...", data: { is_banned: int } }
    """
    user = User.query.get(user_id)

    if not user:
        return jsonify({"code": 404, "message": "用户不存在"}), 404

    if user.username == "admin":
        return jsonify({"code": 400, "message": "不能封禁管理员账号"}), 400

    # 切换封禁状态
    user.is_banned = 1 if user.is_banned == 0 else 0
    db.session.commit()

    action = "已封禁" if user.is_banned == 1 else "已解封"
    return jsonify({
        "code": 200,
        "message": f"用户「{user.username}」{action}",
        "data": {"is_banned": user.is_banned},
    })


# ================== 电影管理 ==================

@api_bp.route("/admin/movies", methods=["GET"])
@admin_required
def admin_movies():
    """
    获取所有电影列表（后台管理用）

    Query Parameters:
        keyword: str    - 搜索关键词（可选）

    Response:
        { code: 200, data: { movies: [...] } }
    """
    keyword = (request.args.get("keyword", "") or "").strip()

    query = Movie.query

    if keyword:
        from sqlalchemy import or_
        query = query.filter(
            or_(
                Movie.title.like(f"%{keyword}%"),
                Movie.info.like(f"%{keyword}%"),
            )
        )

    movies = query.order_by(Movie.id.desc()).all()

    return jsonify({
        "code": 200,
        "data": {
            "movies": [m.to_dict() for m in movies],
        },
    })


@api_bp.route("/admin/movies", methods=["POST"])
@admin_required
def admin_create_movie():
    """
    新增电影（支持海报和视频上传）

    Request: multipart/form-data
        title: str          - 电影标题
        info: str           - 电影简介
        category: str       - 电影分类
        poster: File        - 海报图片
        video: File         - 视频文件（可选）
        is_banner: int      - 是否设为 Banner (0/1)
        banner_order: int   - Banner 排序

    Response:
        { code: 200, message: "添加成功", data: { ... } }
    """
    from flask import current_app

    title = (request.form.get("title") or "").strip()
    info = (request.form.get("info") or "").strip()
    category = (request.form.get("category") or "").strip()
    is_banner = int(request.form.get("is_banner", 0))
    banner_order = int(request.form.get("banner_order", 0))

    if not title or not category:
        return jsonify({"code": 400, "message": "标题和分类不能为空"}), 400

    # 处理海报上传
    poster_filename = ""
    poster_file = request.files.get("poster")
    if poster_file and poster_file.filename:
        poster_filename = "movie_pic/" + secure_filename(poster_file.filename)
        save_path = os.path.join(
            current_app.static_folder, "movie_pic", secure_filename(poster_file.filename),
        )
        os.makedirs(os.path.dirname(save_path), exist_ok=True)
        poster_file.save(save_path)

    # 处理视频上传
    video_filename = None
    video_file = request.files.get("video")
    if video_file and video_file.filename:
        video_filename = secure_filename(video_file.filename)
        save_path = os.path.join(
            current_app.static_folder, "movie_video", video_filename,
        )
        os.makedirs(os.path.dirname(save_path), exist_ok=True)
        video_file.save(save_path)

    movie = Movie(
        title=title,
        info=info,
        poster=poster_filename,
        category=category,
        is_banner=is_banner,
        banner_order=banner_order,
        filename=video_filename,
    )
    db.session.add(movie)
    db.session.commit()

    return jsonify({
        "code": 200,
        "message": "电影添加成功",
        "data": movie.to_dict(),
    })


@api_bp.route("/admin/movies/<int:movie_id>", methods=["PUT"])
@admin_required
def admin_update_movie(movie_id: int):
    """
    编辑电影信息

    Path Parameters:
        movie_id: int       - 电影 ID

    Request: multipart/form-data
        title: str          - 电影标题
        info: str           - 电影简介
        category: str       - 电影分类
        poster: File        - 新海报（可选）
        video: File         - 新视频（可选）
        is_banner: int      - 是否设为 Banner
        banner_order: int   - Banner 排序

    Response:
        { code: 200, message: "修改成功", data: { ... } }
    """
    from flask import current_app

    movie = Movie.query.get(movie_id)
    if not movie:
        return jsonify({"code": 404, "message": "电影不存在"}), 404

    # 更新基本信息
    movie.title = (request.form.get("title") or "").strip() or movie.title
    movie.info = (request.form.get("info") or "").strip() or movie.info
    movie.category = (request.form.get("category") or "").strip() or movie.category
    movie.is_banner = int(request.form.get("is_banner", movie.is_banner))
    movie.banner_order = int(request.form.get("banner_order", movie.banner_order))

    # 更新海报
    poster_file = request.files.get("poster")
    if poster_file and poster_file.filename:
        poster_filename = "movie_pic/" + secure_filename(poster_file.filename)
        save_path = os.path.join(
            current_app.static_folder, "movie_pic", secure_filename(poster_file.filename),
        )
        os.makedirs(os.path.dirname(save_path), exist_ok=True)
        poster_file.save(save_path)
        movie.poster = poster_filename

    # 更新视频
    video_file = request.files.get("video")
    if video_file and video_file.filename:
        video_filename = secure_filename(video_file.filename)
        save_path = os.path.join(
            current_app.static_folder, "movie_video", video_filename,
        )
        os.makedirs(os.path.dirname(save_path), exist_ok=True)
        video_file.save(save_path)
        movie.filename = video_filename

    db.session.commit()

    return jsonify({
        "code": 200,
        "message": "电影修改成功",
        "data": movie.to_dict(),
    })


@api_bp.route("/admin/movies/<int:movie_id>", methods=["DELETE"])
@admin_required
def admin_delete_movie(movie_id: int):
    """
    删除电影

    Path Parameters:
        movie_id: int   - 电影 ID

    Response:
        { code: 200, message: "删除成功" }
    """
    movie = Movie.query.get(movie_id)

    if not movie:
        return jsonify({"code": 404, "message": "电影不存在"}), 404

    db.session.delete(movie)
    db.session.commit()

    return jsonify({"code": 200, "message": f"电影「{movie.title}」已删除"})


# ================== 评论管理 ==================

@api_bp.route("/admin/comments", methods=["GET"])
@admin_required
def admin_comments():
    """
    获取所有评论（后台管理用，支持按电影筛选和关键词搜索）

    Query Parameters:
        movie_id: int   - 电影 ID 筛选（可选）
        keyword: str    - 搜索关键词（可选）

    Response:
        { code: 200, data: { comments: [...] } }
    """
    from sqlalchemy import or_

    movie_id = request.args.get("movie_id", type=int)
    keyword = (request.args.get("keyword", "") or "").strip()

    query = Comment.query

    if movie_id:
        query = query.filter(Comment.movie_id == movie_id)

    if keyword:
        query = query.filter(Comment.content.like(f"%{keyword}%"))

    comments = query.order_by(Comment.created_at.desc()).all()

    return jsonify({
        "code": 200,
        "data": {
            "comments": [c.to_dict() for c in comments],
        },
    })


@api_bp.route("/admin/comments/<int:comment_id>", methods=["DELETE"])
@admin_required
def admin_delete_comment(comment_id: int):
    """
    管理员删除评论

    Path Parameters:
        comment_id: int - 评论 ID

    Response:
        { code: 200, message: "删除成功" }
    """
    comment = Comment.query.get(comment_id)

    if not comment:
        return jsonify({"code": 404, "message": "评论不存在"}), 404

    db.session.delete(comment)
    db.session.commit()

    return jsonify({"code": 200, "message": "评论已删除"})
