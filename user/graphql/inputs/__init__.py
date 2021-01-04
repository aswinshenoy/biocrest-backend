import graphene
from chowkidar.graphql.scalars import Upload


class UserCreationInput(graphene.InputObjectType):
    name = graphene.String()
    email = graphene.String(required=True)
    password = graphene.String(required=True)


class UserUpdationInput(UserCreationInput, graphene.InputObjectType):
    name = graphene.String()
    email = graphene.String()
    password = graphene.String()
    type = graphene.Int()
    idCard = Upload()
    phone = graphene.String()


__all__ = [
    'UserCreationInput',
    'UserUpdationInput'
]
