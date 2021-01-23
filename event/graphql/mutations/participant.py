import json

import graphene
from chowkidar.graphql.decorators import login_required
from chowkidar.graphql.exceptions import APIException
from chowkidar.graphql.scalars import Upload
from django.db.models import Q

from event.models import Participant, Submission
from user.models import Team
from ..types import Participant as PT


class EventRegistrationResponse(graphene.ObjectType):
    uuid = graphene.String()


class Participate(
    graphene.Mutation,
    description='Participate for an event'
):
    class Arguments:
        eventID = graphene.ID(required=True)
        teamID = graphene.ID(required=False)
        data = graphene.JSONString()

    Output = PT

    @login_required
    def mutate(self, info, eventID: str, teamID: str = None, data: graphene.JSONString = False) -> EventRegistrationResponse:
        js = None
        if data is not None:
            try:
                js = json.dumps(data)
            except ValueError as e:
                pass
        if teamID is not None:
            if not Team.objects.filter(id=teamID, members__id=info.context.userID).exists():
                raise APIException('Not member of team', code='FORBIDDEN')
        try:
            if teamID is not None:
                p = Participant.objects.get(event_id=eventID, team_id=teamID)
            else:
                p = Participant.objects.get(event_id=eventID, user_id=info.context.userID)
            p.formData = js
            p.save()
            return p
        except Participant.DoesNotExist:
            if teamID is not None:
                return Participant.objects.create(
                    event_id=eventID,
                    formData=js,
                    team_id=teamID
                )
            return Participant.objects.create(
                event_id=eventID,
                formData=js,
                user_id=info.context.userID
            )


class SubmissionUploadMessage(graphene.ObjectType):
    id = graphene.ID()


class Submit(graphene.Mutation):
    class Arguments:
        participantID = graphene.ID(required=True)
        key = graphene.String(required=True)
        file = Upload()
        url = graphene.String()
        isPublic = graphene.Boolean(required=False)

    Output = SubmissionUploadMessage

    @login_required
    def mutate(
        self, info,
        participantID: str,
        key: str,
        file=None,
        url=None,
        isPublic: bool = True
    ) -> SubmissionUploadMessage:
        try:
            participant = Participant.objects.get(Q(id=participantID))
            if (
                (participant.user is not None and participant.user.id == info.context.userID) or
                (participant.team is not None and participant.team.members.filter(id=info.context.userID).exists())
            ):
                try:
                    submission = Submission.objects.get(participant=participant, event=participant.event, key=key)
                    submission.file = file
                    submission.url = url
                    submission.save()
                except Submission.DoesNotExist:
                    submission = Submission.objects.create(
                        participant=participant,
                        event=participant.event,
                        isPublic=isPublic,
                        key=key,
                        file=file,
                        url=url
                    )
                return SubmissionUploadMessage(id=submission.id)
            else:
                raise APIException('Permission denied', code='FORBIDDEN')
        except Participant.DoesNotExist:
            raise APIException('Participant not found', code='NOT_FOUND')


class ParticipantMutations(graphene.ObjectType):
    participate = Participate.Field()
    submit = Submit.Field()


__all__ = [
    'ParticipantMutations'
]
