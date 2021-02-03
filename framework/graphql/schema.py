import graphene
from graphene_django.debug import DjangoDebug

from chowkidar.graphql import AuthMutations
from event.graphql import EventMutations
from event.graphql.queries import EventQueries
from judging.graphql import JudgingMutations
from user.graphql import UserMutations, UserQueries


class Mutation(
    AuthMutations,
    EventMutations,
    JudgingMutations,
    UserMutations
):
    pass


class Query(
    UserQueries,
    EventQueries,
    graphene.ObjectType
):
    debug = graphene.Field(DjangoDebug, name='_debug')


schema = graphene.Schema(mutation=Mutation, query=Query)

__all__ = [
    'schema'
]
