from django.core.management import BaseCommand

from apps.model_provider_mgmt.models import EmbedProvider, EmbedModelChoices, LLMModel, LLMModelChoices, LLMSkill


class Command(BaseCommand):
    help = '初始化模型数据'

    def handle(self, *args, **options):
        obj, created = EmbedProvider.objects.get_or_create(name='text-embedding-ada-002',
                                                           embed_model=EmbedModelChoices.OPENAI)
        if created:
            obj.embed_config = {
                'model': 'text-embedding-ada-002',
                'openai_api_key': 'your_openai_api_key',
                'openai_base_url': 'https://api.openai.com',
            }
            obj.save()

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

        llm_model, created = LLMModel.objects.get_or_create(
            name='GPT-3.5 Turbo 16K',
            llm_model=LLMModelChoices.GPT35_16K,
        )
        if created:
            llm_model.llm_config = {
                'openai_api_key': 'your_openai_api_key',
                'openai_base_url': 'https://api.openai.com',
                'temperature': 0.7,
            }
            llm_model.save()

        prompt = """
你是知识问答助手
    要求：
                1、像专家一样一步一步的思考问题，根据问题的类别选择合适的知识库，不符合要求的答案不要给出
                2、输出的内容要简洁清晰，不能有歧义
   对话记录: 
                {chat_history}
   问题:
                {input}                
   你的回答是:                           
                """
        llm_skill, created = LLMSkill.objects.get_or_create(
            name='开放问答(GPT3.5-16k)',
            llm_model=llm_model,
        )
        if created:
            llm_skill.skill_prompt = prompt
            llm_skill.save()
