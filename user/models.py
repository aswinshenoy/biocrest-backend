from django.contrib.auth.models import AbstractUser
from django.db import models

from user.fields import MediaField
from user.media import UserIDStorage


class User(AbstractUser):
    USER_TYPE_CHOICES = (
        (0, 'Admin'),
        (1, 'Student'),
        (2, 'Academician'),
        (3, 'Industry')
    )

    id = models.BigAutoField(primary_key=True, null=False)
    first_name = None
    last_name = None
    name = models.CharField(max_length=255, default='', blank=True)
    email = models.EmailField(unique=True, null=False, blank=False)
    city = models.CharField(max_length=50, null=True, blank=True)
    state = models.CharField(max_length=50, null=True, blank=True)
    country = models.CharField(max_length=50, default='India', blank=True)
    isEmailVerified = models.BooleanField(default=False)
    phone = models.CharField(max_length=15, blank=True, null=True)
    isPhoneVerified = models.BooleanField(default=False)
    type = models.PositiveSmallIntegerField(choices=USER_TYPE_CHOICES, blank=True, null=True)
    isIDVerified = models.BooleanField(default=False)
    requiresCorrection = models.BooleanField(default=False)
    remarks = models.CharField(max_length=255, default='', blank=True)


class UserIDCard(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    isIDVerified = models.BooleanField(default=False)
    image = MediaField(
        storage=UserIDStorage(),
        max_size=1024 * 1024 * 8,
        content_types=[
            'image/png', 'image/jpeg', 'image/gif', 'image/bmp', 'image/webp',
        ],
        null=True, blank=True
    )
    timestamp = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'user_id_card'
        verbose_name_plural = "User ID Cards"
        verbose_name = "User ID Card"

    def __str__(self):
        return str(self.user.username)


class UserVerificationOTP(models.Model):
    code = models.CharField(max_length=8)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now=True)
    isPhoneOTP = models.BooleanField(default=False)

    class Meta:
        unique_together = [
            ('user', 'isPhoneOTP')
        ]
        db_table = 'user_verification_otp'
        verbose_name_plural = "User Verification OTPs"
        verbose_name = "User Verification OTP"


__all__ = [
    'User',
    'UserIDCard',
    'UserVerificationOTP'
]
