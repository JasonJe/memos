import redis

class RedisQueue(object):
    def __init__(self, name, namespace='queue', **redis_kwargs):
        self.__db = redis.Redis(**redis_kwargs)
        self.key = '%s:%s' %(namespace, name)

    def qsize(self):
        return self.__db.llen(self.key)

    def put(self, item):
        self.__db.rpush(self.key, item)

    def get_wait(self, timeout=None):
        item = self.__db.blpop(self.key, timeout=timeout)
        return item

    def get_nowait(self):
        item = self.__db.lpop(self.key)
        return item

class RedisSet(object):
    def __init__(self, name, namespace='set', **redis_kwargs):
        self.__db = redis.Redis(**redis_kwargs)
        self.name = '%s:%s' %(namespace, name)

    def size(self):
        return self.__db.scard(self.name)

    def add(self, value):
        self.__db.sadd(self.name, value)

    def get_rand(self):
        return self.__db.srandmember(self.name, 1)[0].decode('utf-8')

    def remove(self, value):
        self.__db.srem(self.name, value)
