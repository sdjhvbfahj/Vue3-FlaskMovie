"""
评论相关 API 路由
处理评论的创建、查询和删除
"""

from flask import request, jsonify, g

from .. import db
from ..models import Comment, Movie
from ..auth import login_required
from . import api_bp


@api_bp.route("/movies/<int:movie_id>/comments", methods=["GET"])
def get_comments(movie_id: int):
    """
    获取电影评论列表

    Path Parameters:
        movie_id: int   - 电影 ID

    Query Parameters:
        page: int        - 页码（默认 1）
        per_page: int    - 每页数量（默认 20）

    Response:
        { code: 200, data: { comments: [...], pagination: { ... } } }
    """
    page = request.args.get("page", 1, type=int)
    per_page = request.args.get("per_page", 20, type=int)

    # 确保电影存在
    movie = Movie.query.get(movie_id)
    if not movie:
        return jsonify({"code": 404, "message": "电影不存在"}), 404

    # 分页查询评论，按时间倒序
    pagination = (
        Comment.query
        .filter_by(movie_id=movie_id)
        .order_by(Comment.created_at.desc(), Comment.id.desc())
        .paginate(page=page, per_page=per_page, error_out=False)
    )

    return jsonify({
        "code": 200,
        "data": {
            "comments": [c.to_dict() for c in pagination.items],
            "pagination": {
                "page": pagination.page,
                "per_page": pagination.per_page,
                "total": pagination.total,
                "pages": pagination.pages,
                "has_prev": pagination.has_prev,
                "has_next": pagination.has_next,
            },
        },
    })


@api_bp.route("/movies/<int:movie_id>/comments", methods=["POST"])
@login_required
def create_comment(movie_id: int):
    """
    创建评论

    Path Parameters:
        movie_id: int   - 电影 ID

    Request Body (JSON):
        content: str    - 评论内容

    Response:
        { code: 200, message: "评论成功", data: { ... } }
        { code: 400, message: "错误信息" }
    """
    data = request.get_json()
    content = (data.get("content") or "").strip() if data else ""

    if not content:
        return jsonify({"code": 400, "message": "评论内容不能为空"}), 400

    # 确保电影存在
    movie = Movie.query.get(movie_id)
    if not movie:
        return jsonify({"code": 404, "message": "电影不存在"}), 404

    # 创建评论
    comment = Comment(
        content=content,
        user=g.current_username,
        movie_id=movie_id,
    )
    db.session.add(comment)
    db.session.commit()

    return jsonify({
        "code": 200,
        "message": "评论成功",
        "data": comment.to_dict(),
    })


@api_bp.route("/comments/<int:comment_id>", methods=["DELETE"])
@login_required
def delete_comment(comment_id: int):
    """
    删除评论

    只有评论作者本人或管理员可以删除

    Path Parameters:
        comment_id: int - 评论 ID

    Response:
        { code: 200, message: "删除成功" }
        { code: 403, message: "无权限" }
    """
    comment = Comment.query.get(comment_id)

    if not comment:
        return jsonify({"code": 404, "message": "评论不存在"}), 404

    # 权限检查：只有评论作者或管理员可以删除
    if comment.user != g.current_username and g.current_username != "admin":
        return jsonify({"code": 403, "message": "无权限删除此评论"}), 403

    db.session.delete(comment)
    db.session.commit()

    return jsonify({
        "code": 200,
        "message": "删除成功",
    })
