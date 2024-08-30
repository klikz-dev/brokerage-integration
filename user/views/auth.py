from django.shortcuts import get_object_or_404

import random
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework import status, serializers
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import default_token_generator
from dj_rest_auth.registration.views import RegisterView
from dj_rest_auth.views import UserDetailsView

from portfolio.utils import IsOwnerPermission
from user.models import CustomUser
from user.serializers.auth import (
                            PasswordResetSerializer, 
                            PasswordResetConfirmSerializer, 
                            EmailSendSerializer, 
                            EmailVerifySerializer, 
                            PhoneSendSerializer, 
                            PhoneVerifySerializer,
                            CustomUserPutPatchSerializer,
                            CustomUserDetailsSerializer)

from utils import email, sms


class CustomRegistration(RegisterView):
    def perform_create(self, serializer):
        # Check if the email already exists before attempting to create a new user
        if CustomUser.objects.filter(email=serializer.validated_data['email']).exists():
            raise serializers.ValidationError({'email': 'This email is already registered.'})
        user = super().perform_create(serializer)
        self.custom_function(user)
        return user

    def custom_function(self, user):
        email_code = str(random.randint(100000, 999999))

        email.sendEmail(
            subject='Your Portfolio Matrix Email verification code',
            message=None,
            html_message=render_to_string('send_verification_email.html', {
                'user': user,
                'email_code': email_code
            }),
            to=user.email
        )

        user.email_code = email_code
        user.email_verified = False
        user.save()


class CustomUserDetailsView(UserDetailsView):
    permission_classes = [IsOwnerPermission]

    def get_serializer_class(self):
        if self.request.method in ['PUT', 'PATCH']:
            return CustomUserPutPatchSerializer
        return CustomUserDetailsSerializer

    def get_object(self):
        return self.request.user

    # Define PUT to explicitly use the serializer and save the object
    def put(self, request, *args, **kwargs):
        user = self.get_object()
        serializer = self.get_serializer_class()(user, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

    def patch(self, request, *args, **kwargs):
        user = self.get_object()
        serializer = self.get_serializer_class()(user, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)


class PasswordReset(APIView):

    permission_classes = [AllowAny]

    queryset = CustomUser.objects.all()
    serializer_class = PasswordResetSerializer

    def post(self, request, *args, **kwargs):

        serializer = PasswordResetSerializer(data=request.data)

        if serializer.is_valid():
            users = CustomUser.objects.all()
            user = get_object_or_404(
                users, email=serializer.validated_data['email'])

            email.sendEmail(
                subject='Password Reset',
                message=None,
                html_message=render_to_string('password_reset_email.html', {
                    'user': user,
                    'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                    'token': default_token_generator.make_token(user),
                    'frontend_url': 'https://portfoliomatrix.com',
                }),
                to=user.email
            )

            return Response(status=status.HTTP_200_OK)

        return Response(serializer.errors)


class PasswordResetConfirm(APIView):
    permission_classes = [AllowAny]

    queryset = CustomUser.objects.all()
    serializer_class = PasswordResetConfirmSerializer

    def post(self, request, *args, **kwargs):
        serializer = PasswordResetConfirmSerializer(data=request.data)

        if serializer.is_valid():
            uid = serializer.validated_data['uid']
            token = serializer.validated_data['token']
            new_password1 = serializer.validated_data['new_password1']
            new_password2 = serializer.validated_data['new_password2']

            users = CustomUser.objects.all()
            user = get_object_or_404(
                users, pk=urlsafe_base64_decode(uid).decode())

            if default_token_generator.check_token(user, token):
                new_password1 = serializer.validated_data['new_password1']
                new_password2 = serializer.validated_data['new_password2']

                if new_password1 == new_password2:
                    user.set_password(new_password1)
                    user.save()

                    return Response(status=status.HTTP_200_OK)

            return Response(status=status.HTTP_400_BAD_REQUEST)

        return Response(serializer.errors)


class SendEmailCode(APIView):

    permission_classes = [IsAuthenticated]

    queryset = CustomUser.objects.all()
    serializer_class = EmailSendSerializer

    def post(self, request, *args, **kwargs):

        serializer = EmailSendSerializer(data=request.data)

        if serializer.is_valid():
            user = request.user
            email_code = str(random.randint(100000, 999999))

            email.sendEmail(
                subject='Your Portfolio Matrix Email verification code',
                message=None,
                html_message=render_to_string('send_verification_email.html', {
                    'user': user,
                    'email_code': email_code
                }),
                to=user.email
            )

            user.email_code = email_code
            user.email_verified = False
            user.save()

            return Response(status=status.HTTP_200_OK)

        return Response(serializer.errors)


class VerifyEmailCode(APIView):

    permission_classes = [IsAuthenticated]

    queryset = CustomUser.objects.all()
    serializer_class = EmailVerifySerializer

    def post(self, request, *args, **kwargs):
        serializer = EmailVerifySerializer(
            data=request.data, partial=True)

        if serializer.is_valid():
            user = request.user
            email_code = serializer.validated_data['email_code']

            if email_code == user.email_code:
                user.email_verified = True
                user.email_code = None
                user.save()
                return Response(status=status.HTTP_200_OK)
            else:
                return Response(status=status.HTTP_400_BAD_REQUEST)

        return Response(serializer.errors)


class SendSMSCode(APIView):

    permission_classes = [IsAuthenticated]

    queryset = CustomUser.objects.all()
    serializer_class = PhoneSendSerializer

    def post(self, request, *args, **kwargs):

        serializer = PhoneSendSerializer(data=request.data)

        if serializer.is_valid():
            user = request.user

            phone_number = serializer.validated_data['phone_number']
            sms_code = str(random.randint(100000, 999999))

            sms.sendSMS(phone_number=phone_number,
                        message=f"Your Portfolio Matrix verification code is {sms_code}")

            user.phone_number = phone_number
            user.sms_code = sms_code
            user.sms_verified = False
            user.save()

            return Response(status=status.HTTP_200_OK)

        return Response(serializer.errors)


class VerifySMSCode(APIView):

    permission_classes = [IsAuthenticated]

    queryset = CustomUser.objects.all()
    serializer_class = PhoneVerifySerializer

    def post(self, request, *args, **kwargs):
        serializer = PhoneVerifySerializer(
            data=request.data, partial=True)

        if serializer.is_valid():
            user = request.user
            sms_code = serializer.validated_data['sms_code']

            if sms_code == user.sms_code:
                user.sms_verified = True
                user.sms_code = None
                user.save()
                return Response(status=status.HTTP_200_OK)
            else:
                return Response(status=status.HTTP_400_BAD_REQUEST)

        return Response(serializer.errors)
