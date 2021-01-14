import graphene
from .participant import ParticipantQueries
from .event import EventQueries as EQ


class EventQueries(
    EQ,
    ParticipantQueries,
    graphene.ObjectType
):
    pass


__all__ = [
    'EventQueries'
]
