from django.conf import settings
from django.db import models
from django.utils import timezone
from django.core.exceptions import ValidationError
from .constants import SOURCE_CHOICES, TRANSACTION_TYPE_CHOICES


class Account(models.Model):
    id = models.CharField(max_length=200, primary_key=True)
    source = models.CharField(max_length=20, choices=SOURCE_CHOICES)
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    buying_power = models.DecimalField(
        max_digits=15, decimal_places=2, null=True, blank=True)
    account_value = models.DecimalField(
        max_digits=15, decimal_places=2, null=True, blank=True)

    def __str__(self):
        return f"{self.name}"

    class Meta:
        verbose_name = "Account"
        verbose_name_plural = "Accounts"


# SECTION - PORTFOLIO AND ASSET GROUP DATA TYPES
class AssetGroup(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE)
    parent_group_id = models.ForeignKey(
        'self', related_name='sub_groups', on_delete=models.CASCADE, null=True, blank=True)
    name = models.CharField(max_length=255, null=False, blank=False)
    color = models.CharField(max_length=7, default=None, null=True, blank=True)
    target_weighting = models.DecimalField(
        max_digits=4, decimal_places=4, null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    sort = models.IntegerField(default=0)

    created_date = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Asset Group"
        verbose_name_plural = "Asset Groups"
        indexes = [
            models.Index(fields=['name']),
            models.Index(fields=['sort']),
        ]
        ordering = ['sort']
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'name'], name='unique_name_per_user')
        ]


# SECTION - ASSET DATA TYPES
class Asset(models.Model):
    id = models.CharField(max_length=200, primary_key=True)
    name = models.CharField(max_length=255)
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE)
    parent_group_id = models.ForeignKey(
        AssetGroup, related_name='%(class)s_assets', on_delete=models.CASCADE, null=True, blank=True)
    target_weighting = models.DecimalField(
        max_digits=4, decimal_places=4, null=True, blank=True)
    color = models.CharField(max_length=7, null=True, blank=True)
    sort = models.IntegerField(default=0)

    created_date = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    class Meta:
        abstract = True


class Symbol(Asset):
    source = models.CharField(
        max_length=20, choices=SOURCE_CHOICES, default='MANUAL')
    ghost = models.BooleanField(default=False)
    account_id = models.ForeignKey(
        Account, related_name='%(class)s_accounts', on_delete=models.CASCADE, null=True, blank=True)
    symbol = models.CharField(max_length=10)
    shares_quantity = models.DecimalField(
        max_digits=15, decimal_places=6, null=True, blank=True)
    equity = models.DecimalField(
        max_digits=15, decimal_places=2, null=True, blank=True)

    def __str__(self):
        return f"{self.symbol} - {self.name}"

    class Meta:
        abstract = True


class Security(Symbol):

    def __str__(self):
        return f"Security: {super().__str__()}"

    class Meta:
        verbose_name = "Security"
        verbose_name_plural = "Securities"
        indexes = [
            models.Index(fields=['symbol']),
        ]


class Crypto(Symbol):

    def __str__(self):
        return f"Crypto: {super().__str__()}"

    class Meta:
        verbose_name = "Crypto"
        verbose_name_plural = "Cryptos"
        indexes = [
            models.Index(fields=['symbol']),
        ]


class OtherAsset(Asset):
    monthly_income = models.DecimalField(
        max_digits=15, decimal_places=2, null=True, blank=True)
    value = models.DecimalField(
        max_digits=15, decimal_places=2, null=True, blank=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Other Asset"
        verbose_name_plural = "Other Assets"
        indexes = [
            models.Index(fields=['name']),
        ]


class Liability(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE)
    parent_group_id = models.ForeignKey(
        AssetGroup, related_name='liabilities', on_delete=models.CASCADE, null=True, blank=True)
    name = models.CharField(max_length=255)
    color = models.CharField(max_length=7, null=True, blank=True)
    target_weighting = models.DecimalField(
        max_digits=5, decimal_places=2, null=True, blank=True)
    monthly_expense = models.DecimalField(
        max_digits=15, decimal_places=2, null=True, blank=True)
    balance = models.DecimalField(
        max_digits=15, decimal_places=2, null=True, blank=True)
    sort = models.IntegerField(default=0)
    created_date = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now=True)

    def __str__(self):
        if self.parent_group_id:
            return f"{self.name} - {self.parent_group_id.user}"
        else:
            return f"{self.name} - No Parent Group"

    class Meta:
        verbose_name = "Liability"
        verbose_name_plural = "Liabilities"
        indexes = [
            models.Index(fields=['name']),
        ]


# SECTION - TRANSACTION DATA TYPE
class Transaction(models.Model):
    security_id = models.ForeignKey(
        'Security', related_name='transactions', on_delete=models.CASCADE, null=True, blank=True)
    other_asset_id = models.ForeignKey(
        'OtherAsset', related_name='transactions', on_delete=models.CASCADE, null=True, blank=True)
    liability_id = models.ForeignKey(
        'Liability', related_name='transactions', on_delete=models.CASCADE, null=True, blank=True)

    transaction_type = models.CharField(
        max_length=20, choices=TRANSACTION_TYPE_CHOICES)
    transaction_date = models.DateTimeField(default=timezone.now)
    amount = models.DecimalField(max_digits=15, decimal_places=2)
    quantity = models.DecimalField(max_digits=15, decimal_places=6)
    description = models.TextField(null=True, blank=True)

    def __str__(self):
        if self.security_id:
            return f"{self.security_id.source} - {self.transaction_type} - {self.amount} - {self.security_id.symbol} - {self.transaction_date}"
        elif self.other_asset_id:
            return f"{self.transaction_type} - {self.amount} - {self.other_asset_id.name} - {self.transaction_date}"
        elif self.liability_id:
            return f"{self.transaction_type} - {self.amount} - {self.liability_id.name} - {self.transaction_date}"
        else:
            return "Invalid Transaction: No linked entity"

    class Meta:
        verbose_name = "Transaction"
        verbose_name_plural = "Transactions"
        indexes = [
            models.Index(fields=['transaction_date']),
        ]

    def clean(self):
        super().clean()
        if not (self.liability_id or self.security_id or self.other_asset_id):
            raise ValidationError(
                'Transaction must be linked to either a liability, security, or other asset.')
        if sum(bool(x) for x in [self.liability_id, self.security_id, self.other_asset_id]) > 1:
            raise ValidationError(
                'Transaction can only be linked to one of liability, security, or other asset.')
