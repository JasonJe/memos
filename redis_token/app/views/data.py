import datetime

from app import auth
from app.models.pipeline import *
from flask import request, make_response, jsonify, Blueprint

d = Blueprint('d', __name__)

@d.route('/', methods = ['GET', 'POST'])
@auth.login_required
def index():
    return 'ok'

@d.route('/data', methods = ['GET'])
@auth.login_required
def data():
    '''
    业务逻辑
    '''
    try:
        data = query_some_data()
        return make_response(jsonify(data))
    except Exception as e:
        return str(e)