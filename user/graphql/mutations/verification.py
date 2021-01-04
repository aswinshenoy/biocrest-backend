import graphene
from chowkidar.graphql.decorators import resolve_user
from chowkidar.graphql.exceptions import APIException

from user.graphql.inputs import UserUpdationInput
from user.models import User


class ApproveRegistration(graphene.Mutation):
    class Arguments:
        userID = graphene.ID(required=True)
        remarks = graphene.String()
        update = graphene.Argument(UserUpdationInput)

    Output = graphene.Boolean

    @resolve_user
    def mutate(self, info, userID, remarks=None, update: UserUpdationInput = None) -> bool:
        if info.context.user.type == 0:
            try:
                user = User.objects.get(id=userID)
                if update:
                    if hasattr(update, "name") and update.name is not None:
                        user.name = update.name
                    if hasattr(update, "type") and update.type is not None:
                        if update.type == 0:
                            raise APIException("Not allowed", code="NOT_ALLOWED")
                        user.type = update.type
                    if hasattr(update, "email") and update.email is not None:
                        if user.email != update.email:
                            user.isEmailVerified = False
                        user.email = update.email
                    if hasattr(update, "phone") and update.phone is not None:
                        if user.phone != update.phone:
                            user.isPhoneVerified = False
                        user.phone = update.phone
                if remarks:
                    user.remarks = remarks
                user.isIDVerified = True
                user.save()
                return True
            except User.DoesNotExist:
                raise APIException('User not found', code='INVALID_ID')
        raise APIException('Not allowed', code='NOT_ALLOWED')


class RejectVerification(graphene.Mutation):
    class Arguments:
        userID = graphene.ID(required=True)
        remarks = graphene.String()

    Output = graphene.Boolean

    @resolve_user
    def mutate(self, info, userID, remarks=None) -> bool:
        if info.context.user.type == 0:
            try:
                user = User.objects.get(id=userID)
                if remarks:
                    user.remarks = remarks
                user.isIDVerified = False
                user.requiresCorrection = True
                user.save()
                return True
            except User.DoesNotExist:
                raise APIException('User not found', code='INVALID_ID')
        raise APIException('Not allowed', code='NOT_ALLOWED')


class VerificationMutations(graphene.ObjectType):
    approveRegistration = ApproveRegistration.Field()
    rejectVerification = RejectVerification.Field()


__all__ = [
    'VerificationMutations'
]
