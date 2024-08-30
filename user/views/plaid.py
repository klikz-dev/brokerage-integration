from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status

import os
import time
import json

import plaid
from plaid.api import plaid_api
from plaid.model.products import Products
from plaid.model.country_code import CountryCode
from plaid.model.item_public_token_exchange_request import ItemPublicTokenExchangeRequest
from plaid.model.link_token_create_request import LinkTokenCreateRequest
from plaid.model.link_token_create_request_user import LinkTokenCreateRequestUser
from plaid.model.investments_holdings_get_request import InvestmentsHoldingsGetRequest
from plaid.model.item_get_request import ItemGetRequest

from drf_spectacular.utils import extend_schema, OpenApiParameter

from user.serializers.plaid import ItemGetSerializer, PublicTokenSerializer, LinkTokenCreateSerializer, InvestmentSerializer
from user.models import Plaid
from portfolio.models import Account, Security, Transaction


PLAID_ENV = os.getenv('PLAID_ENV', 'sandbox')
PLAID_CLIENT_ID = os.getenv('PLAID_CLIENT_ID')
PLAID_SECRET = os.getenv('PLAID_SECRET')
PLAID_VERSION = os.getenv('PLAID_VERSION')
PLAID_REDIRECT_URI = os.getenv('PLAID_REDIRECT_URI')

client = plaid_api.PlaidApi(plaid.ApiClient(plaid.Configuration(
    host=plaid.Environment.Sandbox if PLAID_ENV == 'sandbox' else plaid.Environment.Production,
    api_key={
        'clientId': PLAID_CLIENT_ID,
        'secret': PLAID_SECRET,
        'plaidVersion': PLAID_VERSION
    }
)))


def format_error(e):
    response = json.loads(e.body)
    return {'error': {
        'status_code': e.status,
        'display_message': response['error_message'],
        'error_code': response['error_code'],
        'error_type': response['error_type']
    }}


class GetItems(APIView):
    permission_classes = [IsAuthenticated]
    serializer_class = ItemGetSerializer

    def get(self, request, *args, **kwargs):

        try:
            plaid_tokens = Plaid.objects.filter(user=request.user)

            items = []
            for plaid_token in plaid_tokens:
                item_get_request = ItemGetRequest(
                    access_token=plaid_token.access_token)
                response = client.item_get(item_get_request)
                item = response.to_dict()
                items.append(item)

            return Response(status=status.HTTP_200_OK, data=items)

        except plaid.ApiException as e:
            error_response = format_error(e)
            return JsonResponse(error_response)


class CreateLinkToken(APIView):
    permission_classes = [IsAuthenticated]
    serializer_class = LinkTokenCreateSerializer

    def post(self, request, *args, **kwargs):

        try:
            request_data = LinkTokenCreateRequest(
                client_name="portfolio-matrix",
                products=[
                    Products('auth'),
                    Products('transactions'),
                    Products('investments')
                ],
                country_codes=[CountryCode('US')],
                language='en',
                user=LinkTokenCreateRequestUser(
                    client_user_id=str(time.time())),
                redirect_uri=PLAID_REDIRECT_URI
            )

            response = client.link_token_create(request_data)
            return JsonResponse(response.to_dict())

        except plaid.ApiException as e:
            error_response = format_error(e)
            return JsonResponse(error_response)


class ExchangeAccessToken(APIView):
    permission_classes = [IsAuthenticated]
    serializer_class = PublicTokenSerializer

    def post(self, request, *args, **kwargs):
        serializer = PublicTokenSerializer(data=request.data)

        if serializer.is_valid():
            public_token = serializer.validated_data['public_token']

            try:
                exchange_request = ItemPublicTokenExchangeRequest(
                    public_token=public_token)
                exchange_response = client.item_public_token_exchange(
                    exchange_request)

                access_token = exchange_response['access_token']
                item_id = exchange_response['item_id']

                Plaid.objects.update_or_create(
                    user=request.user,
                    item_id=item_id,
                    defaults={
                        'access_token': access_token
                    }
                )

                return JsonResponse({'access_token_exchange': 'complete'})

            except plaid.ApiException as e:
                error_response = format_error(e)
                return JsonResponse(error_response)

        return Response(serializer.errors)


class GetInvestmentHoldings(APIView):
    permission_classes = [IsAuthenticated]
    serializer_class = InvestmentSerializer

    @extend_schema(
        parameters=[
            OpenApiParameter(
                name='item_id',
                type=str,
                location=OpenApiParameter.QUERY,
                description='Item Id',
                required=True
            ),
        ]
    )
    def get(self, request, *args, **kwargs):
        serializer = InvestmentSerializer(data=request.query_params)

        if serializer.is_valid():
            item_id = serializer.validated_data['item_id']

            try:
                plaid_token = get_object_or_404(
                    Plaid.objects.all(), user=request.user, item_id=item_id)

                holdings_request = InvestmentsHoldingsGetRequest(
                    access_token=plaid_token.access_token)

                response = client.investments_holdings_get(holdings_request)
                return JsonResponse(response.to_dict())

            except plaid.ApiException as e:
                error_response = format_error(e)
                return JsonResponse(error_response)

        return Response(serializer.errors)


class SyncInvestmentHoldings(APIView):
    permission_classes = [IsAuthenticated]
    serializer_class = InvestmentSerializer

    def post(self, request, *args, **kwargs):
        serializer = InvestmentSerializer(data=request.data)

        if serializer.is_valid():
            item_id = serializer.validated_data['item_id']

            try:
                plaid_token = get_object_or_404(
                    Plaid.objects.all(), user=request.user, item_id=item_id)

                holdings_request = InvestmentsHoldingsGetRequest(
                    access_token=plaid_token.access_token)

                response = client.investments_holdings_get(holdings_request)

                # Save Accounts
                for account in response.get('accounts', []):
                    # Data Example
                    # {
                    #     "account_id": "8gANEKBprBtWR5nmD88zhoABjLW1wQCWpbZMx",
                    #     "balances": {
                    #         "available": null,
                    #         "current": 320.76,
                    #         "limit": null,
                    #         "iso_currency_code": "USD",
                    #         "unofficial_currency_code": null
                    #     },
                    #     "mask": "5555",
                    #     "name": "Plaid IRA",
                    #     "official_name": null,
                    #     "type": "investment",
                    #     "subtype": "ira"
                    # }
                    # Data Example

                    Account.objects.update_or_create(
                        id=account.get('account_id'),
                        defaults={
                            'source': 'PLAID',
                            'user': request.user,
                            'name': account.get('name'),
                            'buying_power': account['balances'].get('available'),
                            'account_value': account['balances'].get('current')
                        }
                    )

                # Save Securities
                for security in response.get('securities', []):
                    # Data Example
                    # {
                    #     "security_id": "9EWp9Xpqk1ua6DyXQb89ikMARWA6eyUzAbPMg",
                    #     "isin": null,
                    #     "cusip": null,
                    #     "sedol": null,
                    #     "institution_security_id": null,
                    #     "institution_id": null,
                    #     "proxy_security_id": null,
                    #     "name": "Bitcoin",
                    #     "ticker_symbol": "CUR:BTC",
                    #     "is_cash_equivalent": true,
                    #     "type": "cash",
                    #     "close_price": 39358.09375,
                    #     "close_price_as_of": "2021-05-25",
                    #     "iso_currency_code": "USD",
                    #     "unofficial_currency_code": null,
                    #     "market_identifier_code": null,
                    #     "option_contract": null,
                    #     "update_datetime": null
                    # }
                    # Data Example

                    Security.objects.update_or_create(
                        id=security.get('security_id'),
                        defaults={
                            'source': 'PLAID',
                            'user': request.user,
                            'name': security.get('name') or "Unknown",
                            'symbol': security.get('ticker_symbol') or "Unknown",
                            'color': security.get('type'),
                            'shares_quantity': security.get('close_price'),
                        }
                    )

                # Save Holdings
                for holding in response.get('holdings', []):
                    # Data Example
                    # {
                    #     "account_id": "8gANEKBprBtWR5nmD88zhoABjLW1wQCWpbZMx",
                    #     "security_id": "d6ePmbPxgWCWmMVv66q9iPV94n91vMtov5Are",
                    #     "institution_price": 1,
                    #     "institution_value": 0.01,
                    #     "cost_basis": 1,
                    #     "quantity": 0.01,
                    #     "iso_currency_code": "USD",
                    #     "unofficial_currency_code": null,
                    #     "institution_price_as_of": "2021-05-25",
                    #     "institution_price_datetime": null,
                    #     "vested_quantity": 1,
                    #     "vested_value": 1
                    # }
                    # Data Example

                    try:
                        security = Security.objects.get(
                            id=holding.get('security_id'))
                    except Security.DoesNotExist:
                        continue

                    Transaction.objects.create(
                        security_id=security,
                        amount=holding.get('institution_value'),
                        quantity=holding.get('quantity'),
                    )

                return JsonResponse(response.to_dict())

            except plaid.ApiException as e:
                error_response = format_error(e)
                return JsonResponse(error_response)

        return Response(serializer.errors)
