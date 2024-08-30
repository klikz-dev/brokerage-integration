import os
import logging
import traceback
from django.http import JsonResponse

from django.conf import settings

logger = logging.getLogger(__name__)


class ExceptionLoggingMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        try:
            response = self.get_response(request)
        except Exception as e:
            return self.process_exception(request, e)
        return response

    def process_exception(self, request, exception):

        if settings.DEBUG:
            logger.error("Exception occurred: %s", str(exception))
            logger.error(traceback.format_exc())

            response_data = {
                'error': str(exception),
                'traceback': traceback.format_exc().split('\n')
            }
            return JsonResponse(data=response_data, status=500)
        else:
            logger.error("Exception occurred: %s", str(exception))
            return JsonResponse(data=response_data, status=500)
