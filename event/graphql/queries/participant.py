import graphene
from chowkidar.graphql.decorators import login_required
from chowkidar.graphql.exceptions import APIException
from django.db.models import Q

from event.graphql.inputs import ParticipantQueryFilters
from event.graphql.types import Participant as PType
from event.models import Participant, EventManager
from framework.graphql.types import BaseQuery
from framework.utils.cursor_pagination import CursorPaginator


class ParticipantsQuery(BaseQuery, graphene.ObjectType):
    participants = graphene.List(PType)


class ParticipantQueries(graphene.ObjectType):
    myEventProfile = graphene.Field(
        PType,
        eventID=graphene.ID()
    )
    participants = graphene.Field(
        ParticipantsQuery,
        eventID=graphene.ID(),
        count=graphene.Int(description='Number of challenges to be retrieved'),
        after=graphene.String(),
        search=graphene.String(),
        filters=graphene.Argument(ParticipantQueryFilters)
    )

    @login_required
    def resolve_myEventProfile(self, info, eventID):
        try:
            return Participant.objects.get(
                user_id=info.context.userID,
                event_id=eventID
            )
        except Participant.DoesNotExist:
            raise APIException('You are not a participant in this event', code='NOT_PARTICIPANT')

    @login_required
    def resolve_participants(
        self, info,
        eventID,
        count: int = 25,
        after: str = None,
        search: str = None,
        filters: ParticipantQueryFilters = None
    ):
        qs = Participant.objects.filter(event_id=eventID)
        if EventManager.objects.filter(user_id=info.context.userID, event_id=eventID, canReviewRegistrations=True).exists():
            if filters is not None:
                if filters.type is not None:
                    qs = qs.filter(user__type=filters.type)
                if filters.startDate is not None:
                    qs = qs.filter(timestampRegistered__gte=filters.startDate)
                if filters.endDate is not None:
                    qs = qs.filter(timestampRegistered__lte=filters.endDate)
                if filters.verificationRequired:
                    print('check id is null')
                    qs = qs.exclude(
                        Q(approver__isnull=False) |
                        Q(user__IDCard='') |
                        Q(user__IDCard__exact=None)
                    )
            if search is not None:
                qs = qs.filter(
                    Q(user__username__istartswith=search) |
                    Q(user__name__istartswith=search) |
                    Q(user__phone__contains=search) |
                    Q(user__email__exact=search)
                )
            qs = qs.prefetch_related('user')
            paginator = CursorPaginator(qs, ordering=('timestampRegistered',))
            page = paginator.page(first=count, after=after)
            return ParticipantsQuery(
                participants=page,
                totalCount=qs.count(),
                hasNext=page.has_next,
                lastCursor=paginator.cursor(page[-1]) if page else None
            )
        else:
            raise APIException('You are not allowed to view registrations from this event', code='FORBIDDEN')


__all__ = [
    'ParticipantQueries'
]
