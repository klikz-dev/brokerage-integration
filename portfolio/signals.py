from django.dispatch import receiver
from django.db.models.signals import post_save
from django.conf import settings
from .constants import PORTFOLIO_GROUP_CONFIG, UNGROUPED_GROUP_CONFIG
from .models import AssetGroup

@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_portfolio_group(sender, instance, created, **kwargs):
    if created:
        portfolio_group = AssetGroup.objects.create(user=instance, **PORTFOLIO_GROUP_CONFIG)
        # Now set the parent_group_id for the UNGROUPED_GROUP_CONFIG dynamically
        ungrouped_config = UNGROUPED_GROUP_CONFIG.copy()
        ungrouped_config['parent_group_id'] = portfolio_group  # Use the renamed field
        ungrouped_config['user'] = instance
        AssetGroup.objects.create(**ungrouped_config)
