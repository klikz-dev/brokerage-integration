from dj_rest_auth.registration.serializers import RegisterSerializer
from dj_rest_auth.serializers import UserDetailsSerializer
from rest_framework import serializers

from user.models import Stripe, SnapTrade, CustomUser


class PasswordResetSerializer(serializers.Serializer):
    email = serializers.CharField(required=True, max_length=200)


class PasswordResetConfirmSerializer(serializers.Serializer):
    uid = serializers.CharField(required=True, max_length=200)
    token = serializers.CharField(required=True, max_length=200)
    new_password1 = serializers.CharField(required=True, max_length=200)
    new_password2 = serializers.CharField(required=True, max_length=200)


class UserRegisterSerializer(RegisterSerializer):
    username = None
    first_name = serializers.CharField(required=False, max_length=30)
    last_name = serializers.CharField(required=False, max_length=30)
    preferred_name = serializers.CharField(required=False, max_length=30)
    
    def validate(self, data):
        data.pop('username', None)  # Remove username from data if present
        return super().validate(data)

    def get_cleaned_data(self):
        cleaned_data = super().get_cleaned_data()
        # Explicitly remove username from cleaned_data to avoid any issues
        cleaned_data.pop('username', None)
        cleaned_data['first_name'] = self.validated_data.get('first_name', '')
        cleaned_data['last_name'] = self.validated_data.get('last_name', '')
        cleaned_data['preferred_name'] = self.validated_data.get('preferred_name', '')
        return cleaned_data

    def save(self, request):
        user = super().save(request)
        user.preferred_name = self.cleaned_data.get('preferred_name', '')
        user.save()
        return user


class CustomUserPutPatchSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = 'email', 'first_name', 'last_name', 'phone_number', 'preferred_name'
        read_only_fields = ('pk', 'email_verified', 'sms_verified', 'stripe', 'snaptrade')
        

class CustomUserDetailsSerializer(UserDetailsSerializer):
    class StripeSerializer(serializers.ModelSerializer):
        class Meta:
            model = Stripe
            fields = '__all__'

    class SnapTradeSerializer(serializers.ModelSerializer):
        class Meta:
            model = SnapTrade
            fields = '__all__'

    email_verified = serializers.BooleanField()
    phone_number = serializers.CharField()
    sms_verified = serializers.BooleanField()
    preferred_name = serializers.CharField()
    stripe = StripeSerializer(many=False, read_only=True)
    snaptrade = SnapTradeSerializer(many=False, read_only=True)

    class Meta(UserDetailsSerializer.Meta):
        fields = UserDetailsSerializer.Meta.fields + \
            ('email_verified', 'phone_number',
             'sms_verified', 'preferred_name', 'stripe', 'snaptrade')


class EmailSendSerializer(serializers.Serializer):
    pass


class EmailVerifySerializer(serializers.Serializer):
    email_code = serializers.CharField(required=False, max_length=6)


class PhoneSendSerializer(serializers.Serializer):
    phone_number = serializers.CharField(required=False, max_length=15)


class PhoneVerifySerializer(serializers.Serializer):
    sms_code = serializers.CharField(required=False, max_length=6)
