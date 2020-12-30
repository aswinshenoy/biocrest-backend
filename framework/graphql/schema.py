import graphene
from graphene_django.debug import DjangoDebug

from chowkidar.graphql import AuthMutations
from user.graphql import UserMutations


class Mutation(
    AuthMutations,
    UserMutations
):
    pass


class Query(
    graphene.ObjectType
):
    debug = graphene.Field(DjangoDebug, name='_debug')


schema = graphene.Schema(mutation=Mutation, query=Query)

__all__ = [
    'schema'
]
