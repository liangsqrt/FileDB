from ..urls import add_internal_api
from flask import Blueprint

api = Blueprint("api",__name__)
add_internal_api(api)
