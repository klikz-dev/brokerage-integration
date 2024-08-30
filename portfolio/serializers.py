from rest_framework import serializers
from .models import Account, AssetGroup, Security, Crypto, OtherAsset, Liability, Transaction

class AccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = Account
        fields = '__all__'
        read_only_fields = ('id', 'user', 'created_date', 'modified_date')

class AssetGroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = AssetGroup
        fields = '__all__'
        read_only_fields = ('id', 'user', 'created_date', 'modified_date')

class SecuritySerializer(serializers.ModelSerializer):
    class Meta:
        model = Security
        fields = '__all__'
        read_only_fields = ('id', 'user', 'created_date', 'modified_date', 'source')

class CryptoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Crypto
        fields = '__all__'
        read_only_fields = ('id', 'user', 'created_date', 'modified_date', 'source')

class OtherAssetSerializer(serializers.ModelSerializer):
    class Meta:
        model = OtherAsset
        fields = '__all__'
        read_only_fields = ('id', 'user', 'created_date', 'modified_date',)

class LiabilitySerializer(serializers.ModelSerializer):
    class Meta:
        model = Liability
        fields = '__all__'
        read_only_fields = ('id', 'user', 'created_date', 'modified_date')

class TransactionSerializer(serializers.ModelSerializer):
    security = SecuritySerializer(read_only=True)
    other_asset = OtherAssetSerializer(read_only=True)
    liability = LiabilitySerializer(read_only=True)

    class Meta:
        model = Transaction
        fields = '__all__'
        read_only_fields = ('id', 'user', 'created_date', 'modified_date')
