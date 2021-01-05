from datetime import timedelta

import graphene
from chowkidar.graphql.decorators import resolve_user
from chowkidar.graphql.exceptions import APIException
from django.utils import timezone

from user.graphql.inputs import UserCreationInput, UserUpdationInput
from user.graphql.types import PersonalProfile
from user.models import User, UserIDCard, UserVerificationOTP
from user.tasks import send_otp_to_number, send_email_confirmation_email
from user.utils import generate_username_from_email, generate_otp


class AccountMutationResponse(
    graphene.ObjectType,
    description='Response received on a mutation on account'
):
    success = graphene.Boolean()
    returning = graphene.Field(PersonalProfile, description='User fields to be returned')


class RegisterUser(
    graphene.Mutation,
    description='Creates an user account'
):
    class Arguments:
        input = graphene.Argument(
            UserCreationInput,
            required=True,
            description='Fields accepted to create an user account'
        )

    Output = AccountMutationResponse

    @staticmethod
    def mutate(self, info, input: UserCreationInput) -> AccountMutationResponse:
        if User.objects.filter(email=input.email).exists():
            raise APIException('An account with this email already exist.', code='EMAIL_IN_USE')
        else:
            user = User.objects.create(
                name=input.name,
                email=input.email,
                username=generate_username_from_email(input.email)
            )
            user.set_password(input.password)
            user.save()
            code = generate_otp()
            UserVerificationOTP.objects.create(
                code=code, user=user, isPhoneOTP=False
            )
            print(code)
            #send_email_confirmation_email(user=user, code=code)
            return AccountMutationResponse(success=True, returning=user)


class UpdateProfile(
    graphene.Mutation,
    description='Update profile of a user'
):
    class Arguments:
        update = graphene.Argument(
            UserUpdationInput,
            required=True,
            description='Fields accepted to create an user account'
        )

    Output = AccountMutationResponse

    @resolve_user
    def mutate(self, info, update: UserUpdationInput) -> AccountMutationResponse:
        user = info.context.user
        if hasattr(update, "name") and update.name is not None:
            user.name = update.name
        if hasattr(update, "type") and update.type is not None:
            if update.type == 0:
                raise APIException("Not allowed", code="NOT_ALLOWED")
            user.type = update.type
        if hasattr(update, "email") and update.email is not None:
            if user.email != update.email:
                user.isEmailVerified = False
            user.email = update.email
        if hasattr(update, "city") and update.city is not None:
            user.city = update.city
        if hasattr(update, "state") and update.state is not None:
            user.state = update.state
        if hasattr(update, "country") and update.country is not None:
            user.country = update.country
        if hasattr(update, "password") and update.password is not None:
            user.set_password(update.password)
        if hasattr(update, "idCard") and update.idCard is not None:
            try:
                card = UserIDCard.objects.get(user=user)
                card.image = update.idCard
                card.save()
            except UserIDCard.DoesNotExist:
                UserIDCard.objects.create(
                    user=user,
                    image=update.idCard
                )
        user.requiresCorrection = False
        user.save()
        return AccountMutationResponse(success=True, returning=user)


class ResendOTP(
    graphene.Mutation,
    description='Request for a new OTP for mobile number validation'
):
    class Arguments:
        phone = graphene.String()

    Output = graphene.Boolean

    @resolve_user
    def mutate(self, info, phone: str = None):
        user = info.context.user
        if phone is not None:
            if (not len(phone) == 13) or (not phone.startswith('+91')):
                raise APIException('Invalid phone number', code='INVALID_PHONE_NO')
            if user.phone != phone and User.objects.filter(phone=phone).exists():
                raise APIException('An account with this phone already exist.', code='PHONE_IN_USE')
            user.phone = phone
            user.isPhoneVerified = False
            user.save()
        else:
            if user.isPhoneVerified:
                raise APIException('Phone already verified', code='PHONE_ALREADY_VERIFIED')
        code = generate_otp()
        try:
            entry = UserVerificationOTP.objects.get(user=user, isPhoneOTP=True)
            if entry.timestamp + timedelta(minutes=1) > timezone.now():
                raise APIException('Try after 1 minute', code='TRY_LATER')
            entry.code = code
            entry.timestamp = timezone.now()
            entry.save()
        except UserVerificationOTP.DoesNotExist:
            UserVerificationOTP.objects.create(code=code, user=user, isPhoneOTP=True)
        # send_otp_to_number(code, number=phone)
        print(code)
        return True


class VerifyOTP(
    graphene.Mutation,
    description='Verify the phone number of a user through a confirmation otp sent to it. '
):
    class Arguments:
        otp = graphene.String(
            required=True,
            description='A one time pin code required to verify a phone number.'
        )

    Output = graphene.Boolean

    @resolve_user
    def mutate(self, info, otp):
        user = info.context.user
        try:
            entry = UserVerificationOTP.objects.get(user=user, code=otp, isPhoneOTP=True)
            user.isPhoneVerified = True
            user.save()
            entry.delete()
            return True
        except UserVerificationOTP.DoesNotExist:
            return False


class ResendConfirmationEmail(
    graphene. Mutation,
    description='Request email change of the logged-in user, a confirmation email is send to the new email'
):
    class Arguments:
        email = graphene.String()

    Output = graphene.Boolean

    @resolve_user
    def mutate(self, info, email=None):
        user = info.context.user
        if email is not None:
            if user.email != email and User.objects.filter(email=email).exists():
                raise APIException('An account with this email already exist.', code='EMAIL_IN_USE')
            user.email = email
            user.isEmailVerified = False
            user.save()
        else:
            if user.isEmailVerified:
                raise APIException('Email already verified', code='EMAIL_ALREADY_VERIFIED')
        code = generate_otp()
        try:
            entry = UserVerificationOTP.objects.get(user=user, isPhoneOTP=False)
            if entry.timestamp + timedelta(minutes=1) > timezone.now():
                raise APIException('Try after 1 minute', code='TRY_LATER')
            entry.code = code
            entry.timestamp = timezone.now()
            entry.save()
        except UserVerificationOTP.DoesNotExist:
            UserVerificationOTP.objects.create(
                code=code, user=user, isPhoneOTP=False
            )
        print(code)
        #send_email_confirmation_email(user=user, code=code)
        return True


class VerifyEmail(
    graphene.Mutation,
    description='Verify the ownership of the email by the user through a confirmation otp sent to it. '
):
    class Arguments:
        otp = graphene.String(
            required=True,
            description='A one time pin code required to verify an email.'
        )

    Output = graphene.Boolean

    @resolve_user
    def mutate(self, info, otp):
        user = info.context.user
        try:
            entry = UserVerificationOTP.objects.get(user=user, code=otp, isPhoneOTP=False)
            user.isEmailVerified = True
            user.save()
            entry.delete()
            return True
        except UserVerificationOTP.DoesNotExist:
            return False


class AccountMutations(graphene.ObjectType):
    register = RegisterUser.Field()
    updateProfile = UpdateProfile.Field()
    resendOTP = ResendOTP.Field()
    verifyOTP = VerifyOTP.Field()
    resendConfirmationEmail = ResendConfirmationEmail.Field()
    verifyEmail = VerifyEmail.Field()


__all__ = [
    'AccountMutations'
]
