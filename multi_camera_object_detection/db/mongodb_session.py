from pymongo import MongoClient
import gridfs

class MongoGFS(object):
    def __init__(self, db_name, **mongo_kwargs):
        client = MongoClient(**mongo_kwargs)
        db = client[db_name]
        self.fs = gridfs.GridFS(db)

    def put(self, binary_data, create_time, machine_uuid):
        return self.fs.put(binary_data, create_time = create_time, machine_uuid = machine_uuid)

    def get(self, create_time, machine_uuid):
        file = self.fs.find_one({
                    "create_time": create_time,
                    "machine_uuid": machine_uuid
                })
        binary_data = self.fs.get(file._id).read()
        return binary_data

    def delete(self, create_time, machine_uuid):
        file = self.fs.find_one({
                    "create_time": create_time,
                    "machine_uuid": machine_uuid
                })
        self.fs.delete(file._id)
