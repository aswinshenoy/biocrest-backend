from django.contrib import admin
from user.models import *


@admin.register(AffiliationTitle)
class AffiliationTitleAdmin(admin.ModelAdmin):
    pass


@admin.register(AffiliationBody)
class AffiliationBodyAdmin(admin.ModelAdmin):
    pass


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    pass


@admin.register(Team)
class TeamAdmin(admin.ModelAdmin):
    pass


@admin.register(UserVerificationOTP)
class UserVerificationOTPAdmin(admin.ModelAdmin):
    pass
