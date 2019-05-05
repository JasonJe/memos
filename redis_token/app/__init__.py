import json
import time
from flask import Flask, g
from flask_sqlalchemy import SQLAlchemy
from flask_httpauth import HTTPBasicAuth
from passlib.apps import custom_app_context as pwd_context
from Crypto.Cipher import AES

from app.caches.auth import AESCipher, TokenPool

db = SQLAlchemy()

app = Flask(__name__)
app.config.from_object("settings.Development")

token_pool = TokenPool(app.config['REDIS_HOST'], app.config['REDIS_PORT'], app.config['REDIS_DB'], app.config['REDIS_PASSWORD'])
aesC = AESCipher(app.config['SECRET_KEY'])

class User(db.Model):
    __tablename__ = 'account'
    user_id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(32), index=True)
    password_hash = db.Column(db.String(64))

    def hash_password(self, password):
        '''
        HASH化密码
        '''
        self.password_hash = pwd_context.encrypt(password)

    def verify_password(self, password):
        '''
        密码验证
        '''
        return pwd_context.verify(password, self.password_hash)

    def generate_auth_token(self, expiration = 600):
        '''
        生成token，默认保存600秒
        '''
        info = {'user_id': self.user_id, 'timestamp': time.time()}
        token = aesC.encrypt(json.dumps(info)).decode('utf8')
        token_pool.save_token(self.user_id, token, duration = app.config['TOKEN_DURATION'])
        return token

    @staticmethod
    def verify_auth_token(token):
        '''
        token验证部分
        '''
        try:
            user_id = json.loads(aesC.decrypt(token))['user_id']
            user_info = token_pool.get_uid(user_id, duration = app.config['TOKEN_DURATION'])
            if user_info != {} and user_info[b'token'].decode('utf-8') == token: # 判断当前是否存在token，存在即判断是否与当前token相同（判断是否过期）
                user = User.query.get(user_id)
                return user
            else:
                return False
        except:
            return False
        return False

db.init_app(app)

auth = HTTPBasicAuth()

@auth.verify_password
def verify_password(username_or_token, password):
    '''
    密码验证或token验证函数
    '''
    user = User.verify_auth_token(username_or_token)
    if not user: # 首次验证，验证账号密码
        user = User.query.filter_by(username = username_or_token).first()
        if not user or not user.verify_password(password):
            return False
    g.user = user
    return True

from app.views.auth import a # 验证部分逻辑
from app.views.data import d # 数据部分逻辑

app.register_blueprint(a)
app.register_blueprint(d)