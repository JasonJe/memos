import pymysql

class MysqlDetection(object):
    def __init__(self, **mysql_config):
        self.mysql_kwargs = mysql_config

    def insert_into_detection(self, timestamp, machine_uuid):
        try:
            conn = pymysql.connect(**self.mysql_kwargs)
            with conn.cursor() as cursor:
                stmt = r"INSERT INTO detection (timestamp, machine_uuid, flag) VALUES ('{}', '{}', '0')".format(timestamp, machine_uuid)
                cursor.execute(stmt)
        except expression as e:
            conn.rollback()
        else:
            conn.commit()
        finally:
            conn.close()
    
    def query_filekey(self, timestamp, machine_uuid):
        try:
            conn = pymysql.connect(**self.mysql_kwargs)

            with conn.cursor() as cursor:
                query_stmt = r"SELECT filekey FROM detection WHERE timestamp='{}' AND machine_uuid='{}'".format(timestamp, machine_uuid)
                cursor.execute(query_stmt)
                filekey = cursor.fetchone()
                update_stmt = r"UPDATE detection SET flag='1' WHERE filekey='{}'".format(filekey['filekey'])
                cursor.execute(update_stmt)
            
        except expression as e:
            conn.rollback()
            return 'error'
        else:
            conn.commit()
            return filekey
        finally:
            conn.close()
        
    def inset_into_result(self, xmax, xmin, ymax, ymin, score, object_, filekey):
        try:
            conn = pymysql.connect(**self.mysql_kwargs)
            with conn.cursor() as cursor:
                stmt = r"INSERT INTO result (xmax, xmin, ymax, ymin, score, object, filekey) VALUES ('{}', '{}', '{}', '{}', '{}', '{}', '{}')".format(
                xmax, xmin, ymax, ymin, score, object_, filekey)
                cursor.execute(stmt)
        except expression as identifier:
            conn.rollback()
        else:
            conn.commit()
        finally:
            conn.close()

