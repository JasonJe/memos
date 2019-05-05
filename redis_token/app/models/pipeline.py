import re
import time
import json

from app import db
from app.models.models import *

def query_some_data():
    '''
    数据逻辑部分
    '''
    data = db.session.query(DataTable.test_id, DataTable.test).all()
    return data