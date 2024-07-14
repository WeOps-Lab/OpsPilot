import json

from django.http import JsonResponse
from drf_yasg.utils import swagger_auto_schema
from rest_framework.views import APIView
from drf_yasg import openapi

from apps.bot_mgmt.models import Bot, AutomationSkill
from apps.bot_mgmt.services.automation_service import AutomationService


class AutomationSkillExecuteView(APIView):
    @swagger_auto_schema(
        operation_id="automation_skill_execute",
        operation_description="",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                "bot_id": openapi.Schema(type=openapi.TYPE_STRING, description="机器人ID"),
                "skill_id": openapi.Schema(type=openapi.TYPE_STRING, description="技能ID"),
                "params": openapi.Schema(type=openapi.TYPE_STRING, description="参数"),
                "sender_id": openapi.Schema(type=openapi.TYPE_STRING, description="发送者ID"),
            },
            required=[
                "bot_id",
                "skill_id",
            ],
        ),
    )
    def post(self, request, format=None):
        bot_id = request.data.get("bot_id")
        params = request.data.get("params")
        sender_id = request.data.get("sender_id", "")
        skill_id = request.data.get("skill_id")

        bot = Bot.objects.get(id=bot_id)
        automation_skill = bot.automation_skills.get(skill_id=skill_id)

        salt_skill_config = automation_skill.decrypted_skill_config

        service = AutomationService()
        if params:
            args = params
        else:
            args = salt_skill_config['args']
        result = service.execute_salt_local(
            salt_skill_config['func'], salt_skill_config['tgt'],
            args)
        return JsonResponse(result)
