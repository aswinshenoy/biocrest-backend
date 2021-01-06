import graphene
from chowkidar.graphql.decorators import login_required, resolve_user
from django.db.models import Q

from user.graphql.inputs import ProfileQueryFilters
from user.graphql.types import PersonalProfile, IDVerification, UserProfile, AffiliationDataType
from user.models import AffiliationTitle, AffiliationBody, User, UserIDCard


class UserQueries(graphene.ObjectType):
    me = graphene.Field(PersonalProfile)
    profilesToVerify = graphene.List(IDVerification)
    profiles = graphene.List(
        UserProfile,
        filters=graphene.Argument(ProfileQueryFilters, required=False),
        key=graphene.String(required=False)
    )
    affiliationTitles = graphene.List(
        AffiliationDataType,
        keyword=graphene.String(required=False)
    )
    affiliationBodies = graphene.List(
        AffiliationDataType,
        keyword=graphene.String(required=False)
    )

    def resolve_affiliationTitles(self, info, keyword=None):
        if keyword:
            return AffiliationTitle.objects.filter(name__istartswith=keyword)
        return AffiliationTitle.objects.all()

    def resolve_affiliationBodies(self, info, keyword=None):
        if keyword:
            return AffiliationBody.objects.filter(name__istartswith=keyword)
        return AffiliationBody.objects.all()

    @login_required
    def resolve_me(self, info):
        return User.objects.get(id=info.context.userID)

    @resolve_user
    def resolve_profilesToVerify(self, info):
        if info.context.user.type == 0:
            return UserIDCard.objects.filter(user__isIDVerified=False, user__requiresCorrection=False).order_by('timestamp')
        return None

    @resolve_user
    def resolve_profiles(self, info, filters: ProfileQueryFilters = None, key=None):
        qs = User.objects.exclude(type=0)
        if info.context.user.type == 0:
            if filters is not None:
                if filters.type is not None:
                    qs = qs.filter(type=filters.type)
                if filters.startDate is not None:
                    qs = qs.filter(date_joined__gte=filters.startDate)
                if filters.endDate is not None:
                    qs = qs.filter(date_joined__lte=filters.endDate)
            if key is not None and len(key) > 0:
                qs = qs.filter(
                    Q(username__istartswith=key) |
                    Q(name__istartswith=key) |
                    Q(phone__contains=key) |
                    Q(email__exact=key)
                )
            return qs.order_by('-id')
        return None
