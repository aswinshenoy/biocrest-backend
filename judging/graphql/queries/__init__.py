import graphene
from chowkidar.graphql.decorators import resolve_user
from django.db.models import Avg

from event.graphql.types import Participant
from judging.models import ParticipantJudgement


class JudgedParticipant(graphene.ObjectType):
    avgPoints = graphene.Int()
    noOfJudges = graphene.Int()
    participant = graphene.Field(Participant)

    def resolve_participant(self, info):
        from event.models import Participant as PM
        try:
            return PM.objects.get(id=self['participant'])
        except PM.DoesNotExist:
            pass


class JudgingQueries(graphene.ObjectType):
    scores = graphene.List(
        JudgedParticipant,
        eventID=graphene.ID(required=True)
    )
    eventsToJudge = graphene.List(
        'event.graphql.types.Event'
    )

    @resolve_user
    def resolve_scores(self, info, eventID):
        if info.context.user.type == 0:
            return ParticipantJudgement.objects.filter(
                participant__approver__isnull=False, participant__event_id=eventID
            ).values('participant').order_by('participant').annotate(avgPoints=Avg('points')).order_by('-avgPoints')

    @resolve_user
    def resolve_eventsToJudge(self, info):
        if info.context.user.type == 4:
            from event.models import Event, EventManager
            eventIDs = EventManager.objects.filter(user=info.context.user, canJudgeParticipants=True).values_list('event_id', flat=True)
            print('oomb')
            return Event.objects.filter(id__in=eventIDs)


__all__ = [
    'JudgingQueries'
]