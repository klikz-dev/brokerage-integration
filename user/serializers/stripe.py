from rest_framework import serializers


class WebhookSerializer(serializers.Serializer):
    type = serializers.CharField(required=True, max_length=200)
    data = serializers.JSONField(required=True)
