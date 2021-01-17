import graphene
from chowkidar.graphql.exceptions import APIException

from framework.graphql.types import BaseQuery
from framework.utils.cursor_pagination import CursorPaginator
from ..types import Event as EType
from ...models import Event


class EventsQuery(BaseQuery, graphene.ObjectType):
    events = graphene.List(EType)


class EventQueries(graphene.ObjectType):
    event = graphene.Field(
        EType,
        eventID=graphene.ID(),
        slug=graphene.String(),
        parentID=graphene.ID()
    )
    events = graphene.Field(
        EventsQuery,
        parentID=graphene.ID(required=False),
        count=graphene.Int(description='Number of events to be retrieved'),
        after=graphene.String(),
    )

    @staticmethod
    def resolve_event(self, info, eventID=None, slug=None, parentID=None):
        try:
            if eventID is not None:
                return Event.objects.get(id=eventID)
            if slug is not None:
                return Event.objects.get(slug=slug, parent_id=parentID)
            raise APIException('eventID or slug required', code='BAD_REQUEST')
        except Event.DoesNotExist:
            raise APIException('Event does not exist', code='INVALID_EVENT')

    @staticmethod
    def resolve_events(
        self, info,
        parentID: str = None,
        count: int = 25,
        after: str = None,
    ):
        qs = Event.objects.filter(parent_id=parentID)
        paginator = CursorPaginator(qs, ordering=('id', 'name'))
        page = paginator.page(first=count, after=after)
        return EventsQuery(
            events=page,
            totalCount=qs.count(),
            hasNext=page.has_next,
            lastCursor=paginator.cursor(page[-1]) if page else None
        )


__all__ = [
    'EventQueries'
]
