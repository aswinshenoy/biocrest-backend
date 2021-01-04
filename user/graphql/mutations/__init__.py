import graphene
from .account import *
from .verification import *


class UserMutations(AccountMutations, VerificationMutations, graphene.ObjectType):
    pass


__all__ = [
    'UserMutations'
]
