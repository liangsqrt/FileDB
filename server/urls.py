from server.utils import add_url_include
from .api.zip.urls import *


def add_internal_api(app):
    add_url_include(app, ZIP_MODULE, url_head='/zip', namespace="zip")