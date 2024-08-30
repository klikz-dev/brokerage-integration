from django.http import JsonResponse
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated

from .api import test_tiingo_api



class TiingoTestView(APIView):
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        data = test_tiingo_api()
        return JsonResponse(data, safe=False)
