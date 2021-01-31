from flask import Flask as _Flask, make_response
from flask_script import Manager
from config import *
from server.common import add_blueprint

app = _Flask(
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


if __name__ == '__main__':
    app.run(host="0.0.0.0",port=8002)

