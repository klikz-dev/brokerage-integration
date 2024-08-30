from rest_framework import serializers


class ItemGetSerializer(serializers.Serializer):
    pass  # No additional fields required for retriving items


class LinkTokenCreateSerializer(serializers.Serializer):
    pass  # No additional fields required for creating a link token


class PublicTokenSerializer(serializers.Serializer):
    public_token = serializers.CharField(required=True, max_length=200)


class InvestmentSerializer(serializers.Serializer):
    item_id = serializers.CharField(required=True, max_length=200)
