import graphene
from chowkidar.graphql.decorators import login_required

from user.graphql.types import MyTeamProfile
from user.models import Team


class TeamQueries(graphene.ObjectType):
    myTeams = graphene.List(
        MyTeamProfile
    )

    @login_required
    def resolve_myTeams(self, info):
        print(Team.objects.filter(members=info.context.userID), info.context.userID)
        return Team.objects.filter(members=info.context.userID)


__all__ = [
    'TeamQueries'
]
