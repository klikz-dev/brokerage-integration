from django.contrib import admin
from django.contrib.auth.models import Group
from django.contrib.sites.models import Site
from django.contrib.auth.admin import UserAdmin

from rest_framework.authtoken.models import TokenProxy
from allauth.socialaccount.models import SocialAccount, SocialApp, SocialToken, EmailAddress

from .models import CustomUser, Stripe, SnapTrade, Plaid


@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    model = CustomUser
    list_display = ['username', 'email',
                    'email_verified', 'phone_number', 'sms_verified']
    fieldsets = UserAdmin.fieldsets + (
        (None, {'fields': ('preferred_name', 'email_code', 'email_verified',
         'phone_number', 'sms_code', 'sms_verified')}),
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        (None, {'fields': ('preferred_name', 'email_code', 'email_verified',
         'phone_number', 'sms_code', 'sms_verified')}),
    )


@admin.register(Stripe)
class StripeAdmin(admin.ModelAdmin):
    autocomplete_fields = [
        'user',
    ]

    fieldsets = [
        ('Stripe', {'fields': [
            'subscription',
            'customer',
        ]}),
        ('Status', {'fields': [
            'created',
            'status',
        ]}),
        ('Auth', {'fields': [
            'user',
        ]}),
        ('Address', {'fields': [
            'line1',
            'line2',
            'city',
            'state',
            'postal_code',
            'country',
        ]}),
    ]

    list_display = [
        'user',
        'subscription',
        'customer',
        'line1',
        'city',
        'state',
        'status',
    ]

    list_filter = [
        'status',
    ]

    search_fields = [
        'subscription',
        'customer',
        'line1',
        'line2',
        'city',
        'state',
        'postal_code',
        'country',
    ]


@admin.register(SnapTrade)
class SnapTradeAdmin(admin.ModelAdmin):
    autocomplete_fields = [
        'user',
    ]

    fields = [
        'user',
        'secret'
    ]

    list_display = [
        'user',
    ]


@admin.register(Plaid)
class PlaidAdmin(admin.ModelAdmin):
    autocomplete_fields = [
        'user',
    ]

    fields = [
        'user',
        'access_token',
        'item_id'
    ]

    list_display = [
        'user',
        'access_token',
        'item_id'
    ]


# Unregister the unnecessary pages
admin.site.unregister(Group)
admin.site.unregister(Site)
admin.site.unregister(SocialAccount)
admin.site.unregister(SocialApp)
admin.site.unregister(SocialToken)
admin.site.unregister(EmailAddress)
admin.site.unregister(TokenProxy)
