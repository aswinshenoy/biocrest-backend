import graphene
from .account import *


class UserMutations(AccountMutations, graphene.ObjectType):
    pass


__all__ = [
    'UserMutations'
]
