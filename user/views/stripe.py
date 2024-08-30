from django.shortcuts import get_object_or_404

import os
import stripe
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status

from user.models import CustomUser, Stripe
from user.serializers.stripe import WebhookSerializer

STRIPE_WBH_SEC = os.getenv("STRIPE_WBH_SEC", "")


class Webhook(APIView):

    permission_classes = [IsAuthenticated]

    queryset = Stripe.objects.all()
    serializer_class = WebhookSerializer

    def post(self, request, *args, **kwargs):

        signature = request.META.get('HTTP_STRIPE_SIGNATURE')

        try:
            event = stripe.Webhook.construct_event(
                request.data, signature, STRIPE_WBH_SEC
            )
        except ValueError as e:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        except stripe.error.SignatureVerificationError as e:
            return Response(status=status.HTTP_401_UNAUTHORIZED)

        serializer = WebhookSerializer(data=event, partial=False)

        if serializer.is_valid():
            try:
                webhook_type = serializer.validated_data['type']
                webhook_data = serializer.validated_data['data']

                if webhook_type == "customer.created" or webhook_type == "customer.updated":

                    email = webhook_data['object']['email']

                    users = CustomUser.objects.all()
                    user = get_object_or_404(users, email=email)

                    stripe, _ = Stripe.objects.get_or_create(
                        user=user,
                    )

                    customer = webhook_data['object']['id']
                    stripe.customer = customer

                    address = webhook_data['object']['address']
                    if address:
                        stripe.line1 = address['line1']
                        stripe.line2 = address['line2']
                        stripe.city = address['city']
                        stripe.state = address['state']
                        stripe.postal_code = address['postal_code']
                        stripe.country = address['country']

                    stripe.save()

                    return Response(status=status.HTTP_201_CREATED)

                elif webhook_type == "customer.subscription.created" or webhook_type == "customer.subscription.updated":

                    customer = webhook_data['object']['customer']

                    stripe = get_object_or_404(
                        Stripe.objects.all(), customer=customer)

                    stripe.subscription = webhook_data['object']['id']
                    stripe.status = webhook_data['object']['status']
                    stripe.created = webhook_data['object']['created']

                    stripe.save()

                    return Response(status=status.HTTP_200_OK)

                else:
                    return Response(status=status.HTTP_202_ACCEPTED)

            except Exception as e:
                return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        return Response(serializer.errors)
