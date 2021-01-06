import graphene
from .account import *
from .verification import *
from .affiliation import *


class UserMutations(AccountMutations, VerificationMutations, AffiliationMutations, graphene.ObjectType):
    pass


__all__ = [
    'UserMutations'
]
