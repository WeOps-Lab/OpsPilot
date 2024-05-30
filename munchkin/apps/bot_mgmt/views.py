from django.shortcuts import render
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from langchain.chains.conversation.base import ConversationChain
from langchain.chains.llm import LLMChain
from langchain.memory import ConversationBufferWindowMemory
from langchain_core.prompts import SystemMessagePromptTemplate, HumanMessagePromptTemplate, ChatPromptTemplate, \
    PromptTemplate
from langchain_openai import ChatOpenAI
from rest_framework import serializers
from rest_framework.views import APIView
from langchain.memory import ChatMessageHistory
from rest_framework.viewsets import ModelViewSet

from apps.bot_mgmt.models import Bot
from apps.channel_mgmt.views import ChannelSerializer
from apps.contentpack_mgmt.models import BotActions
from apps.knowledge_mgmt.services import RagService
from apps.model_provider_mgmt.models import LLMModelChoices


class BotSerializer(serializers.ModelSerializer):
    channels = ChannelSerializer(many=True)

    class Meta:
        model = Bot
        fields = '__all__'


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
        converation_history = request.data.get('converation_history', [])

        bot = Bot.objects.filter(id=bot_id).first()
        bot_skill = BotActions.objects.filter(skill_id=skill_id, bot=bot).first()

        if bot_skill.enable_rag:
            rag_context = RagService().rag_serch(ids=[bot.knowledge_base_folders],
                                                 k=bot_skill.rag_top_k,
                                                 num_candidates=bot_skill.rag_num_candidates,
                                                 user_message=user_message)
            rag_result = [x + '\n' for x in rag_context]
            skill_prompt = f"\n\n背景知识:{rag_result}\n\n{bot_skill.action_prompt}"

        if bot.llm_model.llm_model == LLMModelChoices.GPT35_16K:
            client = ChatOpenAI(
                openai_api_key=bot.llm_model.llm_config['openai_api_key'],
                openai_api_base=bot.llm_model.llm_config['openai_base_url'],
                temperature=bot.llm_model.llm_config['temperature'],
                model=bot_skill.llm_model.llm_model
            )

        if bot_skill.enable_conversation_history:
            prompt = PromptTemplate(
                input_variables=["chat_history", "input"],
                template=skill_prompt
            )
            chat_history = ChatMessageHistory()
            for event in converation_history:
                if event['event'] == 'user':
                    chat_history.add_user_message(event['text'])
                elif event['event'] == 'bot':
                    chat_history.add_ai_message(event['text'])

            memory = ConversationBufferWindowMemory(
                memory_key="chat_history", chat_memory=chat_history, k=bot_skill.conversation_window_size
            )
            llm_chain = ConversationChain(llm=client, prompt=prompt, memory=memory, verbose=True)

            result = llm_chain.predict(input=user_message)
        else:
            system_message_prompt = SystemMessagePromptTemplate.from_template(skill_prompt)

            human_template = "{text}"
            human_message_prompt = HumanMessagePromptTemplate.from_template(human_template)
            chat_prompt = ChatPromptTemplate.from_messages([system_message_prompt, human_message_prompt])
            chain = LLMChain(llm=client, prompt=chat_prompt)

            result = chain.run(user_message)

        return {
            "message": result
        }
