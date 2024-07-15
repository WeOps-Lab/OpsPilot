import json

from django.http import JsonResponse
from drf_yasg.utils import swagger_auto_schema
from rest_framework.views import APIView
from drf_yasg import openapi

from apps.bot_mgmt.models import Bot, AutomationSkill
from apps.bot_mgmt.services.automation_service import AutomationService
from loguru import logger


class AutomationSkillExecuteView(APIView):
    @swagger_auto_schema(
        operation_id="automation_skill_execute",
        operation_description="",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                "bot_id": openapi.Schema(type=openapi.TYPE_STRING, description="机器人ID"),
                "skill_id": openapi.Schema(type=openapi.TYPE_STRING, description="技能ID"),
                "params": openapi.Schema(type=openapi.TYPE_OBJECT, description="参数"),
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
        integration = bot.integration.filter(automationskill__skill_id=skill_id).first()
        automation_skill = integration.automationskill_set.get(skill_id=skill_id)

        salt_skill_config = automation_skill.skill_config

        service = AutomationService()
        args = salt_skill_config['args']

        # 获取automation_skill.integration的yml配置，把args中的变量替换
        integration_config = automation_skill.integration.decrypted_integration_config
        for key, value in integration_config.items():
            args = args.replace("{{" + key + "}}", value)

        if params:
            # 替换args字符串中的参数,形式为{{key1}}  {{key2}} key是param的key
            for key, value in params.items():
                args = args.replace("{{" + key + "}}", value)
        logger.info(f"args: {args}")
        result = service.execute_salt_local(
            salt_skill_config['func'], salt_skill_config['tgt'],
            args)
        return JsonResponse(result)
