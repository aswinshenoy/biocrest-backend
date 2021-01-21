import graphene


class TeamProfile(graphene.ObjectType):
    id = graphene.Int()
    name = graphene.String()


class MyTeamProfile(TeamProfile, graphene.ObjectType):
    inviteCode = graphene.String()
    members = graphene.List('user.graphql.types.UserProfile')

    def resolve_members(self, info):
        return self.members.all()


__all__ = [
    'TeamProfile',
    'MyTeamProfile'
]