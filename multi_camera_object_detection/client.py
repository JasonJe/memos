from __future__ import print_function

import grpc
import time
import logging
import cv2
import pickle
import traceback
from proto import RPCserver_pb2_grpc
from proto import RPCserver_pb2
import multiprocessing as mp

def queue_img_put(queue, name, pwd, ip, chan=1):
    cap = cv2.VideoCapture("rtsp://%s:%s@%s//Streaming/Channels/%d" % (name, pwd, ip, chan))
    while True:
        is_opened, frame = cap.read()
        queue.put(cv2.resize(frame, (810, 1440), interpolation=cv2.INTER_CUBIC)) if is_opened else None
        queue.get() if queue.qsize() > 1 else None

def queue_img_get(queue, ip):
    while True:
        frame = queue.get()
        upload_image(frame, ip)

def upload_image(frame, ip):
    with grpc.insecure_channel('localhost:50051') as channel:
        stub = RPCserver_pb2_grpc.ServerInterfaceStub(channel)
        response = stub.ImageStore(
            RPCserver_pb2.UploadRequest(
                binary=pickle.dumps(frame),
                uuid=ip,
                timestamp='{}'.format(time.time())))
        print("Response message:{}".format(response.message))

def run():
    cameras_ip = [] # camera ip list

    with grpc.insecure_channel('localhost:50051') as channel:
        stub = RPCserver_pb2_grpc.ServerInterfaceStub(channel)
        response = stub.TestStatus(RPCserver_pb2.PingRequest())
    print("Greeter client received: " + response.pong)
    
    queues = [mp.Queue(maxsize=2) for _ in cameras_ip]

    processes = []
    for queue, camera_ip in zip(queues, cameras_ip):
        processes.append(mp.Process(target=queue_img_put, args=(queue, "user", "password", camera_ip)))
        processes.append(mp.Process(target=queue_img_get, args=(queue, camera_ip)))

    [setattr(process, "daemon", True) for process in processes]
    [process.start() for process in processes]
    [process.join() for process in processes]

if __name__ == '__main__':
    logging.basicConfig()
    run()
