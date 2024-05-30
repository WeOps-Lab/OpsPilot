from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.knowledge_mgmt.services import RagService


class RagSearchView(APIView):

    @swagger_auto_schema(
        operation_id="rag_search",
        operation_description="知识检索",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                "bot_id": openapi.Schema(type=openapi.TYPE_ARRAY, items=openapi.Schema(type=openapi.TYPE_INTEGER)),
                "action_name": openapi.Schema(type=openapi.TYPE_STRING, description="动作名称"),
                "user_message": openapi.Schema(type=openapi.TYPE_STRING, description="查询内容"),
                "chat_history": openapi.Schema(type=openapi.TYPE_ARRAY, items=openapi.Schema(type=openapi.TYPE_STRING)),
            },
            required=["ids", "action_name", "query"],
        ),
    )
    def post(self, request, format=None):
        context = RagService().bot_action_skill(bot_id=request.data.get('bot_id'),
                                                action_name=request.data.get('action_name'),
                                                user_message=request.data.get('user_message'),
                                                chat_history=request.data.get('chat_history'))
        return Response({"result": context})
