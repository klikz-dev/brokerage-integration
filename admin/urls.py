from django.contrib import admin
from django.urls import path, include
from drf_spectacular.views import SpectacularAPIView, SpectacularRedocView, SpectacularSwaggerView
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenObtainPairView

from user.views.auth import CustomUserDetailsView
from .views import home, custom_yaml, custom_swagger_ui

from portfolio.views import (
    AccountViewSet, AssetGroupViewSet, SecurityViewSet, CryptoViewSet, OtherAssetViewSet, 
    LiabilityViewSet, TransactionViewSet # FetchPortfolio, FetchAllChildren
)

from user.views import auth, stripe, snaptrade, plaid

# from market_data.views import TiingoTestView

# Creating routers for each CRUD group
asset_group_router = DefaultRouter()
asset_group_router.register(r'', AssetGroupViewSet, basename='assetgroup')

security_router = DefaultRouter()
security_router.register(r'', SecurityViewSet, basename='security')

crypto_router = DefaultRouter()
crypto_router.register(r'', CryptoViewSet, basename='crypto')

other_asset_router = DefaultRouter()
other_asset_router.register(r'', OtherAssetViewSet, basename='otherasset')

liability_router = DefaultRouter()
liability_router.register(r'', LiabilityViewSet, basename='liability')

transaction_router = DefaultRouter()
transaction_router.register(r'', TransactionViewSet, basename='transaction')

# URL configuration
urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home, name='home'),

    # OpenAPI Schema and documentation
    path('schema/', SpectacularAPIView.as_view(), name='schema'),
    path('schema/swagger-ui/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    path('schema/redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),
    path('yaml/<str:prefix>', custom_yaml, name='custom_yaml'),
    path('custom-swagger-ui/', custom_swagger_ui, name='custom_swagger_ui'),

    # Authentication
    path(
        'auth/login/',
        TokenObtainPairView.as_view(),
        name='token_obtain_pair'
    ),
    path(
        'auth/password/reset/',
        auth.PasswordReset.as_view(),
        name='password_reset'
    ),
    path(
        'auth/password/reset/confirm/',
        auth.PasswordResetConfirm.as_view(),
        name='password_reset_confirm'
    ),
    path(
        'auth/user/',
        CustomUserDetailsView.as_view(),
        name='user_details'
    ),
    path(
        'auth/',
        include('dj_rest_auth.urls')
    ),
    path(
        'auth/registration/',
        auth.CustomRegistration.as_view(),
        name='account_signup'
    ),
    path(
        'auth/send-email/',
        auth.SendEmailCode.as_view(),
        name='send_email_code'
    ),
    path(
        'auth/verify-email/',
        auth.VerifyEmailCode.as_view(),
        name='verify_email_code'
    ),
    path(
        'auth/send-sms/',
        auth.SendSMSCode.as_view(),
        name='send_sms_code'
    ),
    path(
        'auth/verify-sms/',
        auth.VerifySMSCode.as_view(),
        name='verify_sms_code'
    ),

    # Stripe
    path(
        'stripe/webhook',
        stripe.Webhook.as_view(),
        name='stripe_webhook'
    ),

    # Snaptrade
    path(
        'snaptrade/register',
        snaptrade.Register.as_view(),
        name='snaptrade_register'
    ),
    path(
        'snaptrade/auth',
        snaptrade.Auth.as_view(),
        name='snaptrade_auth'
    ),
    path(
        'snaptrade/accounts',
        snaptrade.ListUserAccounts.as_view(),
        name='snaptrade_list_accounts'
    ),
    path(
        'snaptrade/account/<str:action>',
        snaptrade.GetAccountInformation.as_view(),
        name='snaptrade_get_account_information'
    ),
    path(
        'snaptrade/transactions/history',
        snaptrade.GetTransactionHistory.as_view(),
        name='snaptrade_get_transaction_history'
    ),
    path(
        'snaptrade/sync',
        snaptrade.SyncTransactionHistory.as_view(),
        name='snaptrade_sync'
    ),

    # Plaid
    path(
        'plaid/get-items',
        plaid.GetItems.as_view(),
        name='plaid_get_items'
    ),
    path(
        'plaid/create-link-token',
        plaid.CreateLinkToken.as_view(),
        name='plaid_create_link_token'
    ),
    path(
        'plaid/exchange-access-token',
        plaid.ExchangeAccessToken.as_view(),
        name='plaid_exchange_access_token'
    ),
    path(
        'plaid/get-investment-holdings',
        plaid.GetInvestmentHoldings.as_view(),
        name='plaid_get_investment_holdings'
    ),
    path(
        'plaid/sync-investment-holdings',
        plaid.SyncInvestmentHoldings.as_view(),
        name='plaid_sync_investment_holdings'
    ),

    # SECTION Market data
    #------------------------------------------------------------#
    # path('api/marketdata/test-tiingo/', TiingoTestView.as_view(), name='test_tiingo'),

    # SECTION Asset management groups
    #------------------------------------------------------------#
    # IMPORTANT - MANUALLY DEFINED PATHS OUTSIDE OF ROUTER HAVE
    #               BEEN ADDED SPECIFICALLY TO FIX SCHEMA ISSUES
    
    path(
        'accounts/', AccountViewSet.as_view({
        'get': 'list'}), 
        name='account-list'
    ),
    path(
        'accounts/<int:id>/', AccountViewSet.as_view({
        'get': 'retrieve',
        'delete': 'destroy',}), 
        name='account-detail'
    ),
    path(
        'asset_groups/', AssetGroupViewSet.as_view({
        'get': 'list',
        'post': 'create',}), 
        name='asset-group-list'
    ),
    path(
        'asset_groups/<int:id>/', AssetGroupViewSet.as_view({
        'put': 'update',
        'patch': 'partial_update',
        'delete': 'destroy',}), 
        name='asset-group-detail'
    ),
    path('securities/', include(security_router.urls)),
    path('crypto/', include(crypto_router.urls)),
    path('other_assets/', include(other_asset_router.urls)),
    path('liabilities/', include(liability_router.urls)),
    path('transactions/', include(transaction_router.urls)),

    # Portfolio specific endpoints
    # path('portfolio/fetch-portfolio', FetchPortfolio.as_view(), name='fetch_portfolio'),
    # path('portfolio/fetch-all-children/<int:asset_group_id>/', FetchAllChildren.as_view(), name='fetch_all_children'),
]