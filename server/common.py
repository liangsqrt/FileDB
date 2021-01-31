from server.api import api as api_blueprint
from flask import jsonify

def add_blueprint(app):
    app.register_blueprint(api_blueprint)

