# from django.forms.models import model_to_dict
from rest_framework import permissions
# from django.conf import settings
from .models import AssetGroup
from .constants import PORTFOLIO_GROUP_CONFIG, UNGROUPED_GROUP_CONFIG

# Custom permission to only allow owners of an object to access it.
class IsOwnerPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        # Check if the user is authenticated
        return request.user and request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        # Check that the obj.user is the user making the request
        return obj.user == request.user


# Function to call as a fallback in the event the
# portfolio or ungrouped asset groups are not created or deleted.
# Use as exception in try statements
def ensure_portfolio_ungrouped_exist(user):
    # Ensure "My Portfolio" group exists
    portfolio_group, created = AssetGroup.objects.get_or_create(
        user=user,
        name=PORTFOLIO_GROUP_CONFIG['name'],
        defaults=PORTFOLIO_GROUP_CONFIG
    )

    # Ensure "Ungrouped" group exists
    if 'parent_group_id' not in UNGROUPED_GROUP_CONFIG or UNGROUPED_GROUP_CONFIG['parent_group_id'] is None:
        UNGROUPED_GROUP_CONFIG['parent_group_id'] = portfolio_group

    ungrouped_group, created = AssetGroup.objects.get_or_create(
        user=user,
        name=UNGROUPED_GROUP_CONFIG['name'],
        defaults=UNGROUPED_GROUP_CONFIG
    )

    return portfolio_group, ungrouped_group



"""
def fetch_all_children_data(asset_group):
    # Recursive function to fetch all children of the asset group, assets, liabilities.
    # Fetch includes all children AssetGroups, Assets, Liabilities, and associated transactions
    data = model_to_dict(asset_group, exclude=['user'])
    data['Assets'] = [model_to_dict(
        asset, exclude=['parent_group_id', 'user']) for asset in asset_group.assets.all()]
    data['Liabilities'] = [model_to_dict(
        liability, exclude=['parent_group_id', 'user']) for liability in asset_group.liabilities.all()]
    data['SubGroups'] = [fetch_all_children_data(
        subgroup) for subgroup in asset_group.sub_groups.all()]

    for asset in asset_group.assets.all():
        transactions = asset.transactions.all()
        asset_dict = next(item for item in data['Assets'] if item['id'] == asset.id)
        asset_dict['transactions'] = [model_to_dict(
            transaction, exclude=['security_id', 'other_asset_id', 'liability_id']) for transaction in transactions]

    for liability in asset_group.liabilities.all():
        transactions = liability.transactions.all()
        liability_dict = next(item for item in data['Liabilities'] if item['id'] == liability.id)
        liability_dict['transactions'] = [model_to_dict(
            transaction, exclude=['security_id', 'other_asset_id', 'liability_id']) for transaction in transactions]

    return data
"""