import json

import graphene
from chowkidar.graphql.decorators import login_required

from event.models import Participant
from ..types import Participant as PT


class EventRegistrationResponse(graphene.ObjectType):
    uuid = graphene.String()


class Participate(
    graphene.Mutation,
    description='Participate for an event'
):
    class Arguments:
        eventID = graphene.ID(required=True)
        data = graphene.JSONString()

    Output = PT

    @login_required
    def mutate(self, info, eventID: str, data: graphene.JSONString = False) -> EventRegistrationResponse:
        js = None
        if data is not None:
            try:
                js = json.dumps(data)
            except ValueError as e:
                pass
        try:
            p = Participant.objects.get(event_id=eventID, user_id=info.context.userID)
            p.formData = js
            p.save()
            return p
        except Participant.DoesNotExist:
            return Participant.objects.create(
                event_id=eventID,
                formData=js,
                user_id=info.context.userID
            )


class ParticipantMutations(graphene.ObjectType):
    participate = Participate.Field()


__all__ = [
    'ParticipantMutations'
]
