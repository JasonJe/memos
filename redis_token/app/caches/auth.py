import redis
import base64
from Crypto.Cipher import AES

class AESCipher(object):
    '''
    AES加密部分
    '''
    BS = 16
    pad = lambda self, s: s + (self.BS - len(s) % self.BS) * chr(self.BS - len(s) % self.BS)
    unpad = lambda self, s: s[0:-ord(s[-1])]
    def __init__(self, key):
        self.key = key

    def encrypt(self, text):
        '''
        加密
        '''
        cipher = AES.new(self.key, AES.MODE_ECB)
        raw = self.pad(text)
        enc = cipher.encrypt(raw)
        return base64.b64encode(enc)

    def decrypt(self, text):
        '''
        解密
        '''
        cipher = AES.new(self.key, AES.MODE_ECB)
        enc = base64.b64decode(text)
        return self.unpad(cipher.decrypt(enc).decode('utf-8'))

class TokenPool(object):
    '''
    Redis token存储部分
    '''
    def __init__(self, host, port, db, password):
        self.__db = redis.StrictRedis(connection_pool = 
                        redis.ConnectionPool(host = host, port = port, db = db, password = password))

    def save_token(self, uid, token, duration = 600):
        '''
        以uid为域，'token'为键保存token，默认生存时间为600秒
        '''
        self.__db.hmset(uid, {"token": token})
        self.__db.expire(uid, duration)
        self.__db.save()

    def get_uid(self, uid, duration = 600):
        token_info = self.__db.hgetall(uid)
        if token_info != {}:
            self.__db.expire(uid, duration) # 每次验证成功即进行token生存时间更新
            return token_info
        else:
            return {}
