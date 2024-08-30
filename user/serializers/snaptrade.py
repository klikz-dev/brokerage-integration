from rest_framework import serializers


class RegisterSerializer(serializers.Serializer):
    pass


class AuthSerializer(serializers.Serializer):
    broker = serializers.CharField(required=False, max_length=200)
    reconnect = serializers.CharField(required=False, max_length=200)


class AccountListSerializer(serializers.Serializer):
    pass


class AccountDetailSerializer(serializers.Serializer):
    account_id = serializers.CharField(required=True, max_length=200)


class TransactionHistorySerializer(serializers.Serializer):
    start_date = serializers.DateField(required=False)
    end_date = serializers.DateField(required=False)
    accounts = serializers.CharField(required=False, max_length=2000)
    brokerage_authorizations = serializers.CharField(
        required=False, max_length=2000)
    type = serializers.CharField(required=False, max_length=200)
