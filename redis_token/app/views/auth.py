import datetime

from flask import request, make_response, jsonify, Blueprint, g, url_for, abort

from app.models.pipeline import *
from app import User, auth, app

a = Blueprint('a', __name__, url_prefix='/token')

@a.route('/users', methods=['POST'])
def new_user():
    '''
    注册用户
    '''
    username = request.json.get('un')
    password = request.json.get('pd')
    if username is None or password is None:
        abort(400)
    if User.query.filter_by(username=username).first() is not None:
        abort(400)
    user = User(username=username)
    user.hash_password(password)
    db.session.add(user)
    db.session.commit()
    return (jsonify({'username': user.username}), 201,
            {'Location': url_for('a.get_user', id=user.user_id, _external=True)})

@a.route('/users/<int:id>', methods=['GET'])
@auth.login_required
def get_user(id):
    '''
    查询用户
    '''
    user = User.query.get(id)
    if not user:
        abort(400)
    return jsonify({'username': user.username})

@a.route('', methods=['GET'])
@auth.login_required
def get_auth_token():
    '''
    验证用户账户密码后生成token
    '''
    token = g.user.generate_auth_token(app.config['TOKEN_DURATION'])
    return jsonify({'token': token, 'duration': app.config['TOKEN_DURATION']})

