import graphene
from chowkidar.graphql.decorators import login_required, resolve_user
from django.db.models import Q

from user.graphql.types import PersonalProfile, IDVerification, UserProfile
from user.models import User, UserIDCard


class UserQueries(graphene.ObjectType):
    me = graphene.Field(PersonalProfile)
    profilesToVerify = graphene.List(IDVerification)
    profiles = graphene.List(
        UserProfile,
        key=graphene.String(required=False)
    )

    @login_required
    def resolve_me(self, info):
        return User.objects.get(id=info.context.userID)

    @resolve_user
    def resolve_profilesToVerify(self, info):
        if info.context.user.type == 0:
            return UserIDCard.objects.filter(user__isIDVerified=False, user__requiresCorrection=False).order_by('timestamp')
        return None

    @resolve_user
    def resolve_profiles(self, info, key=None):
        qs = User.objects.exclude(type=0)
        if info.context.user.type == 0:
            if key is not None:
                return qs.filter(
                    Q(username__istartswith=key) |
                    Q(name__istartswith=key) |
                    Q(phone__contains=key) |
                    Q(email__exact=key)
                )[:10]
            else:
                return qs.order_by('-id')
        return None
