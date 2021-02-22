from server.utils import add_url_include
from .api.zip.urls import *
from .graphql.test.urls import GRAPHQL_MODULE


def add_internal_api(app):
    add_url_include(app, ZIP_MODULE, url_head='/zip', namespace="zip")
    add_url_include(app, GRAPHQL_MODULE, url_head='/graphql_head', namespace="graphql_namespace")