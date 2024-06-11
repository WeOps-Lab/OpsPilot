from django.http import JsonResponse
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import viewsets
from rest_framework.decorators import action

from apps.model_provider_mgmt.models import LLMSkill
from apps.model_provider_mgmt.services.llm_service import llm_service


class LLMViewSet(viewsets.ViewSet):

    @action(methods=["post"], detail=False, url_path="execute")
    @swagger_auto_schema(
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                "llm_skill_id": openapi.Schema(type=openapi.TYPE_INTEGER),
                "user_message": openapi.Schema(type=openapi.TYPE_STRING),
                "chat_history": openapi.Schema(type=openapi.TYPE_ARRAY, items=openapi.Schema(type=openapi.TYPE_OBJECT)),
                "super_system_prompt": openapi.Schema(type=openapi.TYPE_STRING),
            },
        ),
    )
    def execute(self, request):
        user_message = request.data.get("user_message")

        # chat_history is [{"event":"user","text":"hello"},{"event":"bot","text":"hi"}]
        chat_history = request.data.get("chat_history")
        super_system_prompt = request.data.get("super_system_prompt", None)

        llm_skill_id = request.data.get("llm_skill_id")
        llm_skill = LLMSkill.objects.get(id=llm_skill_id)

        result = llm_service.chat(llm_skill, user_message, chat_history, super_system_prompt)
        return JsonResponse({"result": result})
