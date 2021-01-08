import graphene
from chowkidar.graphql.decorators import login_required

from user.graphql.types import PersonalProfile, AffiliationDataType
from user.models import AffiliationTitle, AffiliationBody, User


class UserQueries(graphene.ObjectType):
    affiliationTitles = graphene.List(
        AffiliationDataType,
        keyword=graphene.String(required=False)
    )
    affiliationBodies = graphene.List(
        AffiliationDataType,
        keyword=graphene.String(required=False)
    )
    me = graphene.Field(PersonalProfile)

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
