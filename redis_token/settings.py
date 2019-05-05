class Base(object):
    SECRET_KEY = "1234567890123456"

class Product(Base):
    """
    线上环境
    """
    pass

class Testing(Base):
    """
    测试环境
    """
    SQLALCHEMY_DATABASE_URI = 'postgresql://user:password@host:port/db'
    
    TOKEN_DURATION = 60
    
    REDIS_HOST = 'localhost'
    REDIS_PORT = '6379'
    REDIS_DB = 0
    REDIS_PASSWORD = 'password'

    DEBUG = False

class Development(Base):
    """
    开发环境
    """
    SQLALCHEMY_DATABASE_URI = 'postgresql://user:password@host:port/db'
    
    TOKEN_DURATION = 60
    
    REDIS_HOST = 'localhost'
    REDIS_PORT = '6379'
    REDIS_DB = 0
    REDIS_PASSWORD = 'password'

    DEBUG = True  # 开启调试
    