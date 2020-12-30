from django.contrib import admin
from user.models import *


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    pass


@admin.register(UserIDCard)
class UserIDCardAdmin(admin.ModelAdmin):
    pass


@admin.register(UserVerificationOTP)
class UserVerificationOTPAdmin(admin.ModelAdmin):
    pass
