from server import graphql
from ..test import schema
from flask_graphql import GraphQLView


views1 = GraphQLView(
        schema=schema,
        graphql=True
    ).as_view(name="graphqlene")

GRAPHQL_MODULE = [
    ('/port1', views1, "graphene_name"),
]