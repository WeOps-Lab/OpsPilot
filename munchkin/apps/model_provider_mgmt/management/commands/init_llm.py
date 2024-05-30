from django.core.management import BaseCommand

from apps.model_provider_mgmt.models import EmbedProvider, EmbedModelChoices, LLMModel, LLMModelChoices, LLMSkill


class Command(BaseCommand):
    help = '初始化模型数据'

    def handle(self, *args, **options):
        EmbedProvider.objects.get_or_create(
            name='FastEmbed(BAAI/bge-small-en-v1.5)',
            embed_model=EmbedModelChoices.FASTEMBED,
            embed_config={
                'model': 'BAAI/bge-small-en-v1.5',
            },
            enabled=True
        )
        EmbedProvider.objects.get_or_create(
            name='FastEmbed(BAAI/bge-small-zh-v1.5)',
            embed_model=EmbedModelChoices.FASTEMBED,
            embed_config={
                'model': 'BAAI/bge-small-zh-v1.5',
            },
            enabled=True
        )

        llm_model = LLMModel.objects.create(
            name='GPT-3.5 Turbo 16K',
            llm_model=LLMModelChoices.GPT35_16K,
            llm_config={
                'openai_api_key': 'your_openai_api_key',
                'openai_base_url': 'https://api.openai.com',
                'temperature': 0.7,
            }
        )

        prompt = """
        你是WeOps运维小助手，你只能够回复与WeOps有关的问题，不是WeOps的问题，你都会回复：我不清楚。
                要求：
                1、像专家一样一步一步的思考问题，根据问题的类别选择合适的知识库，不符合要求的答案不要给出
                2、你对敏感信息有很强的保密意识，包括客户名称，所以对于回复的答案中用“某客户”代替具体的客户名称
                3、你需要对你给客户的解答负责，否则地球会毁灭，假如知识库中没有提及的，回复：需要联系产品团队进行确认
                4、输出的内容要简洁清晰，不能有歧义
                对话记录: 
                {chat_history}

                问题:
                  {input}                
                """
        LLMSkill.objects.get_or_create(
            name='LLM技能',
            llm_model=llm_model,
            skill_prompt=prompt
        )
