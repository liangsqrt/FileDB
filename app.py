from datetime import datetime
from decimal import Decimal
from logging.config import dictConfig
from bson import ObjectId
from flask import Flask as _Flask, make_response
from flask.json import JSONEncoder
import yaml
from flask_script import Manager
from config import *


class CustomJSONEncoder(JSONEncoder):
    def default(self, o):  # pylint: disable=method-hidden
        if isinstance(o, Decimal):
            res = float(o)
        elif isinstance(o, ObjectId):
            res = str(o)
        else:
            res = JSONEncoder.default(self, o)
        return res

class Flask(_Flask):
    json_encoder = CustomJSONEncoder

app = Flask(  # pylint: disable=invalid-name
    __name__,
)

manager = Manager(app)

@manager.option('-h', '--host', dest='host', default='0.0.0.0')
@manager.option('-p', '--port', dest='port', default='9988')
def run(host, port):
    if not host:
        host = HOST
    if not port:
        port = PORT
    app.run(host, port)


@app.after_request
def af_request(resp):
    """
    #请求钩子，在所有的请求发生后执行，加入headers。
    :param resp:
    :return:
    """
    resp = make_response(resp)
    resp.headers['Access-Control-Allow-Origin'] = '*'
    resp.headers['Access-Control-Allow-Methods'] = 'GET,POST,PUT,DELETE'
    resp.headers[
        'Access-Control-Allow-Headers'] = 'x-requested-with,content-type'
    return resp


add_blueprint(app)
register_error_handler(app)

