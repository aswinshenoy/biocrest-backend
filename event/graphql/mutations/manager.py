import graphene
from chowkidar.graphql.decorators import login_required
from chowkidar.graphql.exceptions import APIException
from django.utils import timezone

from event.models import Participant
from event.tasks import (
    send_email_requesting_correction,
    send_email_confirming_registration,
    send_status_to_number
)
from user.graphql.inputs import UserUpdationInput


class ReviewParticipant(graphene.Mutation):
    class Arguments:
        participantID = graphene.ID(required=True)
        approve = graphene.Boolean(
            required=True
        )
        remarks = graphene.String()
        formUpdate = graphene.JSONString()
        profileUpdate = graphene.Argument(UserUpdationInput)

    Output = graphene.Boolean

    @login_required
    def mutate(
        self, info,
        participantID: graphene.ID, approve: bool,
        remarks=None,
        formUpdate=None, profileUpdate: UserUpdationInput = None
    ) -> bool:
        try:
            reg = Participant.objects.get(id=participantID)
            if reg.event.eventmanager_set.filter(user_id=info.context.userID, canReviewRegistrations=True).exists():
                user = reg.user
                team = reg.team
                if approve:
                    if profileUpdate and user:
                        if hasattr(profileUpdate, "name") and profileUpdate.name is not None:
                            user.name = profileUpdate.name
                        if hasattr(profileUpdate, "type") and profileUpdate.type is not None:
                            if profileUpdate.type == 0:
                                raise APIException("Not allowed", code="NOT_ALLOWED")
                            user.type = profileUpdate.type
                        if hasattr(profileUpdate, "email") and profileUpdate.email is not None:
                            if user.email != profileUpdate.email:
                                user.isEmailVerified = False
                            user.email = profileUpdate.email
                        if hasattr(profileUpdate, "phone") and profileUpdate.phone is not None:
                            if profileUpdate.phone != profileUpdate.phone:
                                user.isPhoneVerified = False
                            user.phone = profileUpdate.phone
                        user.save()
                    if formUpdate:
                        reg.formData = formUpdate
                    reg.approver_id = info.context.userID
                    reg.timestampApproved = timezone.now()
                    reg.save()
                    if user:
                        if user.phone and user.isPhoneVerified:
                            send_status_to_number(number=user.phone, isApproved=True, name=reg.event.name)
                        send_email_confirming_registration(user=user, participant=reg)
                    elif team:
                        if team.leader and team.leader.phone and team.leader.isPhoneVerified:
                            send_status_to_number(number=team.leader.phone, isApproved=True, name=reg.event.name)
                        for m in team.members.all():
                            send_email_confirming_registration(user=m, participant=reg)
                    return True
                else:
                    reg.remarks = remarks
                    reg.save()
                    editURL = 'https://events.amritauniversity.info/edit-profile'
                    if reg.event.parent is not None:
                        editURL = 'https://events.amritauniversity.info/register/' + reg.event.slug
                    if user:
                        if user.phone and user.isPhoneVerified:
                            send_status_to_number(number=user.phone, isApproved=False, name=reg.event.name)
                        send_email_requesting_correction(user=user, participant=reg, editURL=editURL)
                    elif team:
                        if team.leader and team.leader.phone and team.leader.isPhoneVerified:
                            send_status_to_number(number=team.leader.phone, isApproved=False, name=reg.event.name)
                        for m in team.members.all():
                            send_email_confirming_registration(user=m, participant=reg)
                    return True
            else:
                raise APIException('You are not allowed to review registrations', code='FORBIDDEN')
        except Participant.DoesNotExist:
            raise APIException('Participant not found', code='REG_NOT_FOUND')


class ManagerMutations(graphene.ObjectType):
    reviewParticipant = ReviewParticipant.Field()


__all__ = [
    'ManagerMutations'
]
