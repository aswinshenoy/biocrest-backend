import graphene
from .participant import ParticipantQueries


class EventQueries(
    ParticipantQueries,
    graphene.ObjectType
):
    pass


__all__ = [
    'EventQueries'
]
