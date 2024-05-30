from django.http import JsonResponse
from rest_framework import status


class WebUtils:
    @staticmethod
    def response_success(response_data={}, meta={}):
        return JsonResponse({
            'meta': meta,
            'data': response_data,
            'result': True,
            'message': ''
        }, status=status.HTTP_200_OK)

    @staticmethod
    def response_error(response_data={}, error_message='', status=status.HTTP_400_BAD_REQUEST):
        return JsonResponse({
            'data': response_data,
            'result': False,
            'message': error_message
        }, status=status)
