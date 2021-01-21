import graphene
import uuid
from chowkidar.graphql.decorators import resolve_user
from chowkidar.graphql.exceptions import APIException

from user.graphql.types import MyTeamProfile
from user.models import Team


class CreateTeam(graphene.Mutation):
    class Arguments:
        name = graphene.String(required=True)

    Output = MyTeamProfile

    @resolve_user
    def mutate(self, info, name):
        t = Team.objects.create(
            name=name,
            leader=info.context.user,
            allowEditing=True,
            inviteCode=str(uuid.uuid4())[:8]
        )
        t.members.add(info.context.user)
        t.save()
        return t


class JoinTeam(graphene.Mutation):
    class Arguments:
        inviteCode = graphene.String(required=True)

    Output = MyTeamProfile

    @resolve_user
    def mutate(self, info, inviteCode):
        try:
            t = Team.objects.get(inviteCode=inviteCode)
            t.members.add(info.context.user)
            t.save()
            return t
        except Team.DoesNotExist:
            raise APIException('Team does not exist', code='INVALID_INVITE_CODE')


class TeamMutations(graphene.ObjectType):
    createTeam = CreateTeam.Field()
    joinTeam = JoinTeam.Field()


__all__ = [
    'TeamMutations'
]
