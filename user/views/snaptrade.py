import os
from snaptrade_client import SnapTrade as SnapTradeClient
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from drf_spectacular.utils import extend_schema, OpenApiParameter

from user.models import CustomUser, SnapTrade
from user.serializers.snaptrade import RegisterSerializer, AuthSerializer, AccountListSerializer, AccountDetailSerializer, TransactionHistorySerializer
from portfolio.models import Account, Security, Transaction

SNAPTRADE_CLIENT_ID = os.getenv("SNAPTRADE_CLIENT_ID", "")
SNAPTRADE_CONSUMER_KEY = os.getenv("SNAPTRADE_CONSUMER_KEY", "")

snaptrade_client = SnapTradeClient(
    client_id=SNAPTRADE_CLIENT_ID,
    consumer_key=SNAPTRADE_CONSUMER_KEY
)


class Register(APIView):
    permission_classes = [IsAuthenticated]

    queryset = CustomUser.objects.all()
    serializer_class = RegisterSerializer

    def post(self, request, *args, **kwargs):

        serializer = RegisterSerializer(data=request.data)

        if serializer.is_valid():
            snaptrade, _ = SnapTrade.objects.get_or_create(
                user=request.user,
            )

            if not snaptrade.secret:
                response = snaptrade_client.authentication.register_snap_trade_user(
                    user_id=f"pm-{request.user.email}",
                )
                print(response)
                snaptrade.secret = response.body["userSecret"]
                snaptrade.save()

                return Response(status=status.HTTP_201_CREATED)
            else:
                return Response(status=status.HTTP_403_FORBIDDEN)

        return Response(serializer.errors)


class Auth(APIView):
    permission_classes = [IsAuthenticated]

    queryset = CustomUser.objects.all()
    serializer_class = AuthSerializer

    def post(self, request, *args, **kwargs):

        serializer = AuthSerializer(data=request.data)

        if serializer.is_valid():
            broker = serializer.validated_data.get('broker', '')
            reconnect = serializer.validated_data.get('reconnect', '')

            snaptrade, _ = SnapTrade.objects.get_or_create(
                user=request.user,
            )

            if snaptrade.secret:
                response = snaptrade_client.authentication.login_snap_trade_user(
                    user_id=f"pm-{request.user.email}",
                    user_secret=snaptrade.secret,
                    broker=broker,
                    immediate_redirect=False,
                    reconnect=reconnect
                )
                return Response(status=status.HTTP_200_OK, data=response.body)
            else:
                return Response(status=status.HTTP_403_FORBIDDEN)

        return Response(serializer.errors)


class ListUserAccounts(APIView):
    permission_classes = [IsAuthenticated]
    serializer_class = AccountListSerializer

    def get(self, request, *args, **kwargs):

        serializer = AccountListSerializer(data=request.query_params)

        if serializer.is_valid():
            snaptrade, _ = SnapTrade.objects.get_or_create(
                user=request.user,
            )

            if snaptrade.secret:
                response = snaptrade_client.connections.list_brokerage_authorizations(
                    user_id=f"pm-{request.user.email}",
                    user_secret=snaptrade.secret,
                )
                return Response(status=status.HTTP_200_OK, data=response.body)
            else:
                return Response(status=status.HTTP_403_FORBIDDEN)

        return Response(serializer.errors)


class GetAccountInformation(APIView):
    permission_classes = [IsAuthenticated]
    serializer_class = AccountDetailSerializer

    action_methods = {
        'get-user-holdings': 'get_user_holdings',
        'get-user-account-details': 'get_user_account_details',
        'get-user-account-balance': 'get_user_account_balance',
        'get-user-account-positions': 'get_user_account_positions',
        'get-user-account-orders': 'get_user_account_orders',
    }

    @extend_schema(
        parameters=[
            OpenApiParameter(
                name='account_id',
                type=str,
                location=OpenApiParameter.QUERY,
                description='Account Id',
                required=True
            ),
            OpenApiParameter(
                name='action',
                type=str,
                location=OpenApiParameter.PATH,
                description='Get user account information',
                required=True,
                enum=['get-user-holdings', 'get-user-account-details',
                      'get-user-account-balance', 'get-user-account-positions', 'get-user-account-orders']
            ),
        ],
    )
    def get(self, request, *args, **kwargs):
        action = kwargs.get('action')
        if action not in self.action_methods:
            return Response(status=status.HTTP_404_NOT_FOUND)

        serializer = AccountDetailSerializer(data=request.query_params)

        if serializer.is_valid():
            account_id = serializer.validated_data['account_id']

            snaptrade, _ = SnapTrade.objects.get_or_create(user=request.user)

            if snaptrade.secret:
                method_to_call = getattr(
                    snaptrade_client.account_information, self.action_methods[action])
                response = method_to_call(
                    user_id=f"pm-{request.user.email}", user_secret=snaptrade.secret, account_id=account_id)
                return Response(status=status.HTTP_200_OK, data=response.body)
            else:
                return Response(status=status.HTTP_403_FORBIDDEN)

        return Response(serializer.errors)


class GetTransactionHistory(APIView):
    permission_classes = [IsAuthenticated]
    serializer_class = TransactionHistorySerializer

    @extend_schema(
        parameters=[
            OpenApiParameter(
                name='start_date',
                type=str,
                location=OpenApiParameter.QUERY,
                description='Date used to specify timeframe for a reporting call (in YYYY-MM-DD format)',
                required=False
            ),
            OpenApiParameter(
                name='end_date',
                type=str,
                location=OpenApiParameter.QUERY,
                description='Date used to specify timeframe for a reporting call (in YYYY-MM-DD format)',
                required=False
            ),
            OpenApiParameter(
                name='accounts',
                type=str,
                location=OpenApiParameter.QUERY,
                description='Optional comma seperated list of account IDs',
                required=False
            ),
            OpenApiParameter(
                name='brokerage_authorizations',
                type=str,
                location=OpenApiParameter.QUERY,
                description='Optional comma seperated list of brokerage authorization IDs',
                required=False
            ),
            OpenApiParameter(
                name='type',
                type=str,
                location=OpenApiParameter.QUERY,
                description='Optional comma seperated list of types to filter activities by. Potential values include - DIVIDEND - BUY - SELL - CONTRIBUTION - WITHDRAWAL - EXTERNAL_ASSET_TRANSFER_IN - EXTERNAL_ASSET_TRANSFER_OUT - INTERNAL_CASH_TRANSFER_IN - INTERNAL_CASH_TRANSFER_OUT - INTERNAL_ASSET_TRANSFER_IN - INTERNAL_ASSET_TRANSFER_OUT - INTEREST - REBATE - GOV_GRANT - TAX - FEE - REI - FXT',
                required=False,
            ),
        ],
    )
    def get(self, request, *args, **kwargs):
        serializer = TransactionHistorySerializer(data=request.query_params)

        if serializer.is_valid():
            snaptrade, _ = SnapTrade.objects.get_or_create(user=request.user)

            start_date = serializer.validated_data.get('start_date')
            end_date = serializer.validated_data.get('end_date')
            accounts = serializer.validated_data.get('accounts')
            brokerage_authorizations = serializer.validated_data.get(
                'brokerage_authorizations')
            type = serializer.validated_data.get('type')

            if snaptrade.secret:
                response = snaptrade_client.transactions_and_reporting.get_activities(
                    user_id=f"pm-{request.user.email}",
                    user_secret=snaptrade.secret,
                    start_date=start_date,
                    end_date=end_date,
                    accounts=accounts,
                    brokerage_authorizations=brokerage_authorizations,
                    type=type
                )
                return Response(status=status.HTTP_200_OK, data=response.body)
            else:
                return Response(status=status.HTTP_403_FORBIDDEN)

        return Response(serializer.errors)


class SyncTransactionHistory(APIView):
    permission_classes = [IsAuthenticated]
    serializer_class = TransactionHistorySerializer

    def post(self, request, *args, **kwargs):
        serializer = TransactionHistorySerializer(data=request.query_params)

        if serializer.is_valid():
            snaptrade, _ = SnapTrade.objects.get_or_create(user=request.user)

            if snaptrade.secret:
                # Save Account
                accounts = snaptrade_client.account_information.list_user_accounts(
                    user_id=f"pm-{request.user.email}",
                    user_secret=snaptrade.secret,
                )

                for account in accounts:
                    # Data Example
                    # [
                    #     {
                    #         "id": "917c8734-8470-4a3e-a18f-57c3f2ee6631",
                    #         "brokerage_authorization": "87b24961-b51e-4db8-9226-f198f6518a89",
                    #         "portfolio_group": "2bcd7cc3-e922-4976-bce1-9858296801c3",
                    #         "name": "Robinhood Individual",
                    #         "number": "Q6542138443",
                    #         "institution_name": "Robinhood",
                    #         "created_date": "2024-07-23T22:50:22.761Z",
                    #         "meta": {
                    #             "type": "Margin",
                    #             "status": "ACTIVE",
                    #             "institution_name": "Robinhood"
                    #         },
                    #         "cash_restrictions": [],
                    #         "sync_status": {
                    #             "transactions": {
                    #                 "initial_sync_completed": true,
                    #                 "last_successful_sync": "2022-01-24",
                    #                 "first_transaction_date": "2022-01-24"
                    #             },
                    #             "holdings": {
                    #                 "initial_sync_completed": true,
                    #                 "last_successful_sync": "2024-06-28 18:42:46.561408+00:00"
                    #             }
                    #         },
                    #         "balance": {
                    #             "total": {
                    #                 "amount": 15363.23,
                    #                 "currency": "USD"
                    #             }
                    #         }
                    #     }
                    # ]
                    # Data Example

                    Account.objects.update_or_create(
                        id=account.get('id'),
                        defaults={
                            'source': 'SNAPTRADE',
                            'user': request.user,
                            'name': account.get('name'),
                            'buying_power': account['balance'].get('total').get('amount'),
                        }
                    )

                # Save Security
                ### Todo ###

                # Save Transaction
                transactions = snaptrade_client.transactions_and_reporting.get_activities(
                    user_id=f"pm-{request.user.email}",
                    user_secret=snaptrade.secret,
                )

                for transaction in transactions:
                    # Data Example
                    # [
                    #     {
                    #         "id": "2f7dc9b3-5c33-4668-3440-2b31e056ebe6",
                    #         "account": {
                    #             "id": "917c8734-8470-4a3e-a18f-57c3f2ee6631",
                    #             "name": "Robinhood Individual",
                    #             "number": "Q6542138443",
                    #             "sync_status": {
                    #                 "transactions": {
                    #                     "initial_sync_completed": true,
                    #                     "last_successful_sync": "2022-01-24",
                    #                     "first_transaction_date": "2022-01-24"
                    #                 },
                    #                 "holdings": {
                    #                     "initial_sync_completed": true,
                    #                     "last_successful_sync": "2024-06-28 18:42:46.561408+00:00"
                    #                 }
                    #             }
                    #         },
                    #         "symbol": {
                    #             "id": "2bcd7cc3-e922-4976-bce1-9858296801c3",
                    #             "symbol": "VAB.TO",
                    #             "raw_symbol": "VAB",
                    #             "description": "VANGUARD CDN AGGREGATE BOND INDEX ETF",
                    #             "currency": {
                    #                 "id": "87b24961-b51e-4db8-9226-f198f6518a89",
                    #                 "code": "USD",
                    #                 "name": "US Dollar"
                    #             },
                    #             "exchange": {
                    #                 "id": "2bcd7cc3-e922-4976-bce1-9858296801c3",
                    #                 "code": "TSX",
                    #                 "mic_code": "XTSE",
                    #                 "name": "Toronto Stock Exchange",
                    #                 "timezone": "America/New_York",
                    #                 "start_time": "09:30:00",
                    #                 "close_time": "16:00:00",
                    #                 "suffix": ".TO"
                    #             },
                    #             "type": {
                    #                 "id": "2bcd7cc3-e922-4976-bce1-9858296801c3",
                    #                 "code": "cs",
                    #                 "description": "Common Stock",
                    #                 "is_supported": true
                    #             },
                    #             "figi_code": "BBG000B9XRY4",
                    #             "figi_instrument": {
                    #                 "figi_code": "BBG000B9Y5X2",
                    #                 "figi_share_class": "BBG001S5N8V8"
                    #             }
                    #         },
                    #         "option_symbol": {
                    #             "id": "2bcd7cc3-e922-4976-bce1-9858296801c3",
                    #             "ticker": "SPY 220819P00200000",
                    #             "option_type": "CALL",
                    #             "strike_price": 200,
                    #             "expiration_date": "2026-12-18",
                    #             "is_mini_option": false,
                    #             "underlying_symbol": {
                    #                 "id": "2bcd7cc3-e922-4976-bce1-9858296801c3",
                    #                 "symbol": "SPY",
                    #                 "raw_symbol": "VAB",
                    #                 "description": "SPDR S&P 500 ETF Trust",
                    #                 "currency": {
                    #                     "id": "87b24961-b51e-4db8-9226-f198f6518a89",
                    #                     "code": "USD",
                    #                     "name": "US Dollar"
                    #                 },
                    #                 "exchange": {
                    #                     "id": "2bcd7cc3-e922-4976-bce1-9858296801c3",
                    #                     "code": "ARCX",
                    #                     "mic_code": "ARCA",
                    #                     "name": "NYSE ARCA",
                    #                     "timezone": "America/New_York",
                    #                     "start_time": "09:30:00",
                    #                     "close_time": "16:00:00",
                    #                     "suffix": "None",
                    #                     "allows_cryptocurrency_symbols": false
                    #                 },
                    #                 "type": {
                    #                     "id": "2bcd7cc3-e922-4976-bce1-9858296801c3",
                    #                     "code": "cs",
                    #                     "description": "Common Stock",
                    #                     "is_supported": true
                    #                 },
                    #                 "currencies": [
                    #                     {
                    #                         "id": "87b24961-b51e-4db8-9226-f198f6518a89",
                    #                         "code": "USD",
                    #                         "name": "US Dollar"
                    #                     }
                    #                 ],
                    #                 "figi_code": "BBG000B9XRY4",
                    #                 "figi_instrument": {
                    #                     "figi_code": "BBG000B9Y5X2",
                    #                     "figi_share_class": "BBG001S5N8V8"
                    #                 }
                    #             }
                    #         },
                    #         "price": 0.4,
                    #         "units": 5.2,
                    #         "amount": 263.82,
                    #         "currency": {
                    #             "id": "87b24961-b51e-4db8-9226-f198f6518a89",
                    #             "code": "USD",
                    #             "name": "US Dollar"
                    #         },
                    #         "type": "string",
                    #         "option_type": "BUY_TO_OPEN",
                    #         "description": "WALT DISNEY UNIT DIST ON 21 SHS REC 12/31/21 PAY 01/06/22",
                    #         "trade_date": "2024-03-22T16:27:55.000Z",
                    #         "settlement_date": "2024-03-26T00:00:00.000Z",
                    #         "fee": 0,
                    #         "fx_rate": 1.032,
                    #         "institution": "Robinhood",
                    #         "external_reference_id": "2f7dc9b3-5c33-4668-3440-2b31e056ebe6"
                    #     }
                    # ]
                    # Data Example

                    try:
                        account_id = transaction.get('account').get('id')
                        account = Account.objects.get(id=account_id)
                    except Account.DoesNotExist:
                        continue

                    Transaction.objects.create(
                        security_id=account,
                        amount=transaction.get('institution_value'),
                        quantity=transaction.get('quantity'),
                    )

                return Response(status=status.HTTP_200_OK)
            else:
                return Response(status=status.HTTP_403_FORBIDDEN)

        return Response(serializer.errors)
