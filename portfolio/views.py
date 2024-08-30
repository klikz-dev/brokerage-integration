from rest_framework import viewsets, status
from rest_framework.response import Response

from .constants import PORTFOLIO_GROUP_CONFIG, UNGROUPED_GROUP_CONFIG
from .models import Account, AssetGroup, Security, Crypto, OtherAsset, Liability, Transaction
from .utils import IsOwnerPermission, ensure_portfolio_ungrouped_exist
from .serializers import AccountSerializer, AssetGroupSerializer, SecuritySerializer, CryptoSerializer, OtherAssetSerializer, LiabilitySerializer, TransactionSerializer

# Inherit this base viewset for common fields for all views
#------------------------------------------------------------#

class BaseViewSet(viewsets.ModelViewSet):
    permission_classes = (IsOwnerPermission,)
    
    def perform_create(self, serializer):
        user = self.request.user
        serializer.save(user=user)
        
        # Check if the model has a 'parent_group_id' attribute and it's not set
        if hasattr(serializer.instance, 'parent_group_id') and not serializer.instance.parent_group_id:
            try:
                # Attempt to find the existing 'Ungrouped' group
                ungrouped_group = AssetGroup.objects.get(user=user, name=UNGROUPED_GROUP_CONFIG['name'])
            except AssetGroup.DoesNotExist:
                # If it doesn't exist, ensure it and the portfolio group are properly set up
                _, ungrouped_group = ensure_portfolio_ungrouped_exist(user)

            # Set the 'parent_group_id' to the 'Ungrouped' group and save the instance
            serializer.instance.parent_group_id = ungrouped_group
            serializer.instance.save()
        
#------------------------------------------------------------#


class AccountViewSet(viewsets.ModelViewSet):
    queryset = Account.objects.all()
    serializer_class = AccountSerializer


class AssetGroupViewSet(BaseViewSet):
    serializer_class = AssetGroupSerializer
    permission_classes = [IsOwnerPermission]

    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        protected_names = [PORTFOLIO_GROUP_CONFIG['name'], UNGROUPED_GROUP_CONFIG['name']]
        if instance.name in protected_names:
            return Response(
                {"detail": f"Changes to '{instance.name}' are not allowed."}, status=status.HTTP_403_FORBIDDEN)
        return super().update(request, *args, **kwargs)

    def partial_update(self, request, *args, **kwargs):
        instance = self.get_object()
        protected_names = [PORTFOLIO_GROUP_CONFIG['name'], UNGROUPED_GROUP_CONFIG['name']]
        if instance.name in protected_names:
            return Response(
                {"detail": f"Changes to '{instance.name}' are not allowed."}, status=status.HTTP_403_FORBIDDEN)
        return super().partial_update(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        protected_names = [PORTFOLIO_GROUP_CONFIG['name'], UNGROUPED_GROUP_CONFIG['name']]
        if instance.name in protected_names:
            return Response(
                {"detail": f"Deletion of '{instance.name}' is not allowed."}, status=status.HTTP_403_FORBIDDEN)
        return super().destroy(request, *args, **kwargs)
    
    def get_queryset(self):
        return AssetGroup.objects.filter(user=self.request.user)

class SecurityViewSet(BaseViewSet):
    queryset = Security.objects.all()
    serializer_class = SecuritySerializer

class CryptoViewSet(BaseViewSet):
    queryset = Crypto.objects.all()
    serializer_class = CryptoSerializer

class OtherAssetViewSet(BaseViewSet):
    queryset = OtherAsset.objects.all()
    serializer_class = OtherAssetSerializer

class LiabilityViewSet(BaseViewSet):
    queryset = Liability.objects.all()
    serializer_class = LiabilitySerializer

class TransactionViewSet(viewsets.ModelViewSet):
    queryset = Transaction.objects.all()
    serializer_class = TransactionSerializer
