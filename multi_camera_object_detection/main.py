import time
import ujson

from setting import *
from utils.object_detection import * 
from utils.image_libs import * 
from db.mongodb_session import *
from db.redis_session import *
from db.mysql_session import *

object_session = object_model(MODEL_PATH)
mongogfs = MongoGFS(MONGODB_DB, host = MONGODB_HOST, port = MONGODB_PORT, password = MONGODB_PWD)
queue = RedisQueue('detection', host = REDIS_HOST, port = REDIS_PORT, db = REDIS_DB, password = REDIS_PWD)
db = MysqlDetection(host = MYSQL_HOST, user = MYSQL_USER, password = MYSQL_PWD, db = MYSQL_DB, charset = MYSQL_CHARSET, cursorclass=pymysql.cursors.DictCursor)

def main():
    while True:
        image_meta = queue.get_nowait()
        print("Get image from {}".format(ujson.loads(image_meta)))

        if image_meta is None:
            time.sleep(2)
            continue
        image_meta = ujson.loads(image_meta)

        binary_data = mongogfs.get(image_meta['timestamp'], image_meta['uuid'])
        file_key = db.query_filekey(image_meta['timestamp'], image_meta['uuid'])

        image_np = get_imnp(binary_data)

        boxes, scores, label_id, label_dict = object_session.interface(image_np)
        box_info = object_info(boxes, scores, label_id, label_dict)
        if box_info == []:
            continue
        roi_msg = get_roibox(box_info, image_np)

        for roi in roi_msg:
            db.inset_into_result(
                roi['xmax'], roi['xmin'], roi['ymax'], roi['ymin'], roi['score'], roi['object'], file_key['filekey'])
        print(roi_msg)


if __name__ == "__main__":
    main()