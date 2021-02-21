import graphene
from chowkidar.graphql.decorators import login_required

from event.graphql.types import GalleryItem, Participant


class ParticipantGallery(graphene.ObjectType):
    participant = graphene.Field(Participant)
    submissions = graphene.List(GalleryItem)

    def resolve_participant(self, info):
        return self

    def resolve_submissions(self, info):
        from event.models import Submission
        return Submission.objects.filter(
           isPublic=True, participant=self
        )


class SubmissionQueries(graphene.ObjectType):
    gallery = graphene.List(
        ParticipantGallery,
        eventID=graphene.ID(required=True)
    )

    @login_required
    def resolve_gallery(self, info, eventID):
        from event.models import Participant
        return Participant.objects.filter(
            event_id=eventID,
            approver__isnull=False
        )


__all__ = [
    'SubmissionQueries'
]
