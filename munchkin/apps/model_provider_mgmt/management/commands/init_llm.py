from django.core.management import BaseCommand

from apps.model_provider_mgmt.models import EmbedProvider, EmbedModelChoices, LLMModel, LLMModelChoices, LLMSkill, \
    RerankProvider, RerankModelChoices


class Command(BaseCommand):
    help = '初始化模型数据'

    def handle(self, *args, **options):
        obj, created = RerankProvider.objects.get_or_create(name='bce-reranker-base_v1',
                                                            rerank_model=RerankModelChoices.BCE)
        if created:
            obj.rerank_config = {
                'model': './models/bce-reranker-base_v1',
            }
            obj.save()
        obj, created = EmbedProvider.objects.get_or_create(name='bce-embedding-base_v1',
                                                           embed_model=EmbedModelChoices.BCEEMBEDDING)
        if created:
            obj.embed_config = {
                'model': './models/bce-embedding-base_v1',
            }
            obj.save()

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
            name='GPT-4 32K',
            llm_model=LLMModelChoices.CHAT_GPT,
        )
        if created:
            llm_model.llm_config = {
                'openai_api_key': 'your_openai_api_key',
                'openai_base_url': 'https://api.openai.com',
                'temperature': 0.7,
                'model': 'gpt-4-32k',
            }
            llm_model.save()

        llm_model, created = LLMModel.objects.get_or_create(
            name='GPT-3.5 Turbo 16K',
            llm_model=LLMModelChoices.CHAT_GPT,
        )
        if created:
            llm_model.llm_config = {
                'openai_api_key': 'your_openai_api_key',
                'openai_base_url': 'https://api.openai.com',
                'model': 'gpt-3.5-turbo-16k',
                'temperature': 0.7,
            }
            llm_model.save()

        prompt = """
参考信息：
{chat_history}
---
我的问题或指令：
{input}
---
请根据上述参考信息回答我的问题或回复我的指令。前面的参考信息可能有用，也可能没用，你需要从我给出的参考信息中选出与我的问题最相关的那些，来为你的回答提供依据。回答一定要忠于原文，简洁但不丢信息，不要胡乱编造。我的问题或指令是什么语种，你就用什么语种回复,
你的回复：                                 
                """
        llm_skill, created = LLMSkill.objects.get_or_create(
            name='开放问答(GPT3.5-16k)',
            llm_model=llm_model,
        )
        if created:
            llm_skill.skill_prompt = prompt
            llm_skill.save()
