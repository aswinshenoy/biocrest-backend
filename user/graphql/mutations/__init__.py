import graphene
from .account import *
from .affiliation import *


class UserMutations(AccountMutations, AffiliationMutations, graphene.ObjectType):
    pass


__all__ = [
    'UserMutations'
]
