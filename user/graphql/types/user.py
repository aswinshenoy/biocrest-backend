import graphene
from django.utils import timezone

from user.models import UserIDCard


class UserProfile(graphene.ObjectType):
    id = graphene.ID()
    username = graphene.String()
    name = graphene.String()
    email = graphene.String()
    phone = graphene.String()
    city = graphene.String()
    state = graphene.String()
    country = graphene.String()
    gender = graphene.String()
    type = graphene.String()
    remarks = graphene.String()
    dateJoined = graphene.String()
    isPhoneVerified = graphene.Boolean()
    isEmailVerified = graphene.Boolean()
    isIDVerified = graphene.Boolean()
    requiresCorrection = graphene.Boolean()
    isProfileComplete = graphene.Boolean()

    def resolve_dateJoined(self, info):
        to_tz = timezone.get_default_timezone()
        return self.date_joined.astimezone(to_tz).isoformat()

    def resolve_isProfileComplete(self, info):
        if (
            self.isEmailVerified and
            self.isPhoneVerified and
            self.phone is not None and
            self.type is not None and
            not self.requiresCorrection
        ):
            if UserIDCard.objects.filter(user=self).exists():
                return True
        return False


class PersonalProfile(UserProfile, graphene.ObjectType):
    pass


class IDVerification(graphene.ObjectType):
    user = graphene.Field(UserProfile)
    image = graphene.String()
    timestamp = graphene.String()

    def resolve_image(self, info):
        if self and self.image and hasattr(self.image, 'url') and self.image.url:
            return self.image.url


__all__ = [
    'UserProfile',
    'PersonalProfile',
    'IDVerification'
]
