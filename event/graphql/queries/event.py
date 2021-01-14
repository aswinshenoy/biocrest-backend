import graphene
from chowkidar.graphql.decorators import login_required
from chowkidar.graphql.exceptions import APIException

from ..types import Event as EType
from ...models import Event


class EventQueries(graphene.ObjectType):
    event = graphene.Field(
        EType,
        eventID=graphene.ID(required=True)
    )

    @login_required
    def resolve_event(self, info, eventID):
        try:
            return Event.objects.get(id=eventID)
        except Event.DoesNotExist:
            raise APIException('Event does not exist', code='INVALID_EVENT')


__all__ = [
    'EventQueries'
]
