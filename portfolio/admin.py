from django.contrib import admin
from .models import Account, AssetGroup, Security, Crypto, OtherAsset, Liability, Transaction

# admin.site.register(Portfolio)
admin.site.register(Account)
admin.site.register(AssetGroup)
admin.site.register(Security)
admin.site.register(Crypto)
admin.site.register(OtherAsset)
admin.site.register(Liability)
admin.site.register(Transaction)
