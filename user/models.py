from django.db import models
from django.contrib.auth.models import AbstractUser
from .managers import CustomUserManager


SUBSCRIPTION_STATUS = [
    ("incomplete", "incomplete"),
    ("incomplete_expired", "incomplete_expired"),
    ("trialing", "trialing"),
    ("active", "active"),
    ("past_due", "past_due"),
    ("canceled", "canceled"),
    ("unpaid", "unpaid"),
    ("paused", "paused"),
]


class CustomUser(AbstractUser):
    email = models.EmailField(unique=True, blank=False, null=False)
    
    preferred_name = models.CharField(max_length=200, blank=True, null=True)

    email_code = models.CharField(max_length=15, blank=True, null=True)
    email_verified = models.BooleanField(default=False)

    phone_number = models.CharField(max_length=15, blank=True, null=True)
    sms_code = models.CharField(max_length=15, blank=True, null=True)
    sms_verified = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []
    
    objects = CustomUserManager()
    
    def save(self, *args, **kwargs):
        self.username = self.email  # Set username to be the same as email
        super(CustomUser, self).save(*args, **kwargs)
        
    def __str__(self):
        return self.email


class Stripe(models.Model):
    user = models.OneToOneField(
        CustomUser, related_name="stripe", on_delete=models.CASCADE, blank=False, null=False)

    subscription = models.CharField(
        max_length=200, default=None, blank=True, null=True)
    customer = models.CharField(
        max_length=200, default=None, blank=True, null=True)

    created = models.DateTimeField()
    status = models.CharField(
        max_length=200, choices=SUBSCRIPTION_STATUS, default="active", blank=True, null=True)

    # Address
    line1 = models.CharField(
        max_length=200, default=None, null=True, blank=True)
    line2 = models.CharField(
        max_length=200, default=None, null=True, blank=True)
    city = models.CharField(
        max_length=200, default=None, null=True, blank=True)
    state = models.CharField(
        max_length=200, default=None, null=True, blank=True)
    postal_code = models.CharField(
        max_length=200, default=None, null=True, blank=True)
    country = models.CharField(
        max_length=200, default=None, null=True, blank=True)

    def __str__(self):
        return self.user.email


class SnapTrade(models.Model):
    user = models.OneToOneField(
        CustomUser, related_name="snaptrade", on_delete=models.CASCADE, blank=False, null=False)

    secret = models.CharField(
        max_length=200, default=None, blank=True, null=True)


class Plaid(models.Model):
    user = models.ForeignKey(
        CustomUser, related_name="plaid_accounts", on_delete=models.CASCADE, blank=False, null=False)

    access_token = models.CharField(
        max_length=200, default=None, blank=True, null=True)
    item_id = models.CharField(
        max_length=200, default=None, blank=True, null=True)
