from django.http import JsonResponse
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet

from apps.bot_mgmt.models import Bot
from apps.bot_mgmt.serializers import BotSerializer
from apps.bot_mgmt.services.skill_excute_service import SkillExecuteService


class BotViewSet(ModelViewSet):
    serializer_class = BotSerializer
    queryset = Bot.objects.all()


class SkillExecuteView(APIView):
    @swagger_auto_schema(
        operation_id="skill_execute",
        operation_description="",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                "bot_id": openapi.Schema(type=openapi.TYPE_INTEGER, description="机器人ID"),
                "skill_id": openapi.Schema(type=openapi.TYPE_INTEGER, description="技能ID"),
                "user_message": openapi.Schema(type=openapi.TYPE_STRING, description="用户消息"),
                "converation_history": openapi.Schema(type=openapi.TYPE_ARRAY, description="历史对话",
                                                      items=openapi.Schema(type=openapi.TYPE_STRING)),
            },
            required=["bot_id", "skill_id", "user_message", ],
        ),
    )
    def post(self, request, format=None):
        bot_id = request.data.get('bot_id')
        skill_id = request.data.get('skill_id')
        user_message = request.data.get('user_message')
        sender_id = request.data.get('sender_id', '')
        converation_history = request.data.get('converation_history', [])

        service = SkillExecuteService()
        result = service.execute_skill(bot_id, skill_id, user_message, converation_history, sender_id)

        return JsonResponse({
            "result": result
        })
