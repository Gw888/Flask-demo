from flask import jsonify, request
from app import db
from app.api import api_bp
from app.models.user import User
from app.schemas.user import user_schema, users_schema
from werkzeug.security import generate_password_hash
from sqlalchemy.exc import IntegrityError

@api_bp.route('/users', methods=['GET'])
def get_users():
    """
    获取用户列表，支持分页和搜索。
    请求参数:
        - page: 页码（可选，默认1）
        - page_size: 每页数量（可选，默认10）
        - username: 按用户名模糊搜索（可选）
        - email: 按邮箱模糊搜索（可选）
    返回:
        {
            "code": 200,
            "message": "Success",
            "data": {
                "items": [用户对象列表],
                "total": 总用户数
            }
        }
    """
    page = request.args.get('page', default=1, type=int)
    page_size = request.args.get('page_size', default=10, type=int)
    username = request.args.get('username', default=None, type=str)
    email = request.args.get('email', default=None, type=str)
    query = User.query
    # 支持用户名和邮箱模糊搜索
    if username:
        query = query.filter(User.username.like(f"%{username}%"))
    if email:
        query = query.filter(User.email.like(f"%{email}%"))
    total = query.count()
    users = query.offset((page - 1) * page_size).limit(page_size).all()
    return jsonify({
        'code': 200,
        'message': 'Success',
        'data': {
            'items': users_schema.dump(users),
            'total': total
        }
    })

@api_bp.route('/users/<int:id>', methods=['GET'])
def get_user(id):
    """
    获取单个用户详情。
    请求参数:
        - id: 用户ID（URL路径参数）
    返回:
        {
            "code": 200,
            "message": "Success",
            "data": 用户对象
        }
    """
    user = User.query.get_or_404(id)
    return jsonify({
        'code': 200,
        'message': 'Success',
        'data': user_schema.dump(user)
    })

@api_bp.route('/users', methods=['POST'])
def create_user():
    """
    新增用户。
    请求体:
        {
            "username": "用户名",
            "email": "邮箱",
            "password": "密码"
        }
    返回:
        {
            "code": 201,
            "message": "User created successfully",
            "data": 新增用户对象
        }
    注意：用户名和邮箱必须唯一，后端会校验。
    """
    data = request.get_json()
    # 后端校验用户名和邮箱唯一性
    if User.query.filter_by(username=data['username']).first():
        return jsonify({'code': 400, 'message': '用户名已存在'}), 400
    if User.query.filter_by(email=data['email']).first():
        return jsonify({'code': 400, 'message': '邮箱已存在'}), 400
    try:
        user = User(
            username=data['username'],
            email=data['email'],
            password=generate_password_hash(data['password'])
        )
        db.session.add(user)
        db.session.commit()
        return jsonify({
            'code': 201,
            'message': 'User created successfully',
            'data': user_schema.dump(user)
        }), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({
            'code': 500,
            'message': str(e)
        }), 500

@api_bp.route('/users/<int:id>', methods=['PUT'])
def update_user(id):
    """
    更新用户信息。
    请求参数:
        - id: 用户ID（URL路径参数）
    请求体:
        {
            "username": "新用户名",
            "email": "新邮箱",
            "password": "新密码"（可选）
        }
    返回:
        {
            "code": 200,
            "message": "User updated successfully",
            "data": 更新后的用户对象
        }
    注意：用户名和邮箱必须唯一，后端会校验。
    """
    user = User.query.get_or_404(id)
    data = request.get_json()
    # 后端校验用户名和邮箱唯一性（排除自己）
    if 'username' in data and data['username'] != user.username:
        if User.query.filter_by(username=data['username']).filter(User.id != id).first():
            return jsonify({'code': 400, 'message': '用户名已存在'}), 400
        user.username = data['username']
    if 'email' in data and data['email'] != user.email:
        if User.query.filter_by(email=data['email']).filter(User.id != id).first():
            return jsonify({'code': 400, 'message': '邮箱已存在'}), 400
        user.email = data['email']
    if 'password' in data and data['password']:
        user.password = generate_password_hash(data['password'])
    try:
        db.session.commit()
        return jsonify({
            'code': 200,
            'message': 'User updated successfully',
            'data': user_schema.dump(user)
        })
    except Exception as e:
        db.session.rollback()
        return jsonify({
            'code': 500,
            'message': str(e)
        }), 500

@api_bp.route('/users/<int:id>', methods=['DELETE'])
def delete_user(id):
    """
    删除用户。
    请求参数:
        - id: 用户ID（URL路径参数）
    返回:
        {
            "code": 200,
            "message": "User deleted successfully"
        }
    """
    user = User.query.get_or_404(id)
    try:
        db.session.delete(user)
        db.session.commit()
        return jsonify({
            'code': 200,
            'message': 'User deleted successfully'
        })
    except Exception as e:
        db.session.rollback()
        return jsonify({
            'code': 500,
            'message': str(e)
        }), 500 