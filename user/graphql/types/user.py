import graphene


class UserProfile(graphene.ObjectType):
    id = graphene.ID()
    username = graphene.String()
    name = graphene.String()
    email = graphene.String()
    phone = graphene.String()
    type = graphene.String()
    isPhoneVerified = graphene.Boolean()
    isEmailVerified = graphene.Boolean()
    isIDVerified = graphene.Boolean()


class PersonalProfile(UserProfile, graphene.ObjectType):
    isProfileComplete = graphene.Boolean()

    def resolve_isProfileComplete(self, info):
        if (
            self.isEmailVerified and
            self.isPhoneVerified and
            self.phone is not None and
            self.type is not None
        ):
            return True
        return False


__all__ = [
    'UserProfile',
    'PersonalProfile'
]
