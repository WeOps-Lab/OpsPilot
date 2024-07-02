import json

from django.http import JsonResponse
from drf_yasg.utils import swagger_auto_schema
from rest_framework.views import APIView
from drf_yasg import openapi

from apps.bot_mgmt.services.automation_service import AutomationService


class SaltExecuteView(APIView):
    @swagger_auto_schema(
        operation_id="salt_execute",
        operation_description="",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                "bot_id": openapi.Schema(type=openapi.TYPE_INTEGER, description="机器人ID"),
                "params": openapi.Schema(type=openapi.TYPE_STRING, description="参数"),
                "sender_id": openapi.Schema(type=openapi.TYPE_STRING, description="发送者ID"),
            },
            required=[
                "bot_id",
                "params",
            ],
        ),
    )
    def post(self, request, format=None):
        bot_id = request.data.get("bot_id")
        params = request.data.get("params")
        sender_id = request.data.get("sender_id", "")

        service = AutomationService()
        result = service.execute_salt_local('cmd.run', 'ops-pilot', params)
        return JsonResponse({"result": result})
