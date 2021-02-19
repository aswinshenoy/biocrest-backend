import graphene
from chowkidar.graphql.decorators import login_required

from event.graphql.types import GalleryItem


class SubmissionQueries(graphene.ObjectType):
    gallery = graphene.List(
        GalleryItem,
        eventID=graphene.ID(required=True)
    )

    @login_required
    def resolve_gallery(self, info, eventID):
        from event.models import Submission
        return Submission.objects.filter(
            event_id=eventID,
            isPublic=True,
            participant__approver__isnull=False
        )


__all__ = [
    'SubmissionQueries'
]
