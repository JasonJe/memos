import sys
import time
import grpc
import ujson
import logging

from concurrent import futures

from proto import RPCserver_pb2_grpc
from proto import RPCserver_pb2

from db.mongodb_session import *
from db.redis_session import *
from db.mysql_session import *
from setting import *

mongogfs = MongoGFS(MONGODB_DB, host = MONGODB_HOST, port = MONGODB_PORT, password = MONGODB_PWD)
queue = RedisQueue('detection', host = REDIS_HOST, port = REDIS_PORT, db = REDIS_DB, password = REDIS_PWD)
db = MysqlDetection(host = MYSQL_HOST, user = MYSQL_USER, password = MYSQL_PWD, db = MYSQL_DB, charset = MYSQL_CHARSET, cursorclass=pymysql.cursors.DictCursor)

class ServerInterface(RPCserver_pb2_grpc.ServerInterfaceServicer):
    def TestStatus(self, request, context):
        return RPCserver_pb2.PongReply(
            pong = '{} Server Live'.format(time.time())
        )
    
    def ImageStore(self, request, context):
        mongogfs.put(request.binary, request.timestamp, request.uuid)
        queue.put(ujson.dumps({
            'timestamp': request.timestamp, 
            'uuid': request.uuid
        }))
        db.insert_into_detection(request.timestamp, request.uuid)
        return RPCserver_pb2.ResultReply(
            message = '{} [{}] upload success.'.format(request.uuid, time.time())
        )

def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    RPCserver_pb2_grpc.add_ServerInterfaceServicer_to_server(ServerInterface(), server)
    server.add_insecure_port('[::]:50051')
    server.start()
    try:
        while True:
            time.sleep(10000)
    except KeyboardInterrupt:
        server.stop(0)

if __name__ == '__main__':
    logging.basicConfig()
    serve()

# python -m grpc_tools.protoc -I./ --python_out=. --grpc_python_out=./ RPCserver.proto