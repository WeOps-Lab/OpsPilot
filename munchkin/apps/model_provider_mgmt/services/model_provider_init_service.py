from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token

from apps.model_provider_mgmt.models import (
    EmbedModelChoices,
    EmbedProvider,
    LLMModel,
    LLMModelChoices,
    LLMSkill,
    RerankModelChoices,
    RerankProvider,
)
from apps.model_provider_mgmt.models.ocr_provider import OCRProvider


class ModelProviderInitService:
    def __init__(self, owner: User):
        self.owner = owner

    def init(self):
        if self.owner.username == "admin":
            RerankProvider.objects.get_or_create(
                name="bce-reranker-base_v1",
                rerank_model_type=RerankModelChoices.LANG_SERVE,
                defaults={"rerank_config": {"base_url": "http://bce-rerank-server.ops-pilot:8100"}},
            )

            EmbedProvider.objects.get_or_create(
                name="bce-embedding-base_v1",
                embed_model_type=EmbedModelChoices.LANG_SERVE,
                defaults={
                    "embed_config": {
                        "base_url": "http://bce-embed-server.ops-pilot:8102",
                    }
                },
            )

            EmbedProvider.objects.get_or_create(
                name="FastEmbed(BAAI/bge-small-en-v1.5)",
                embed_model_type=EmbedModelChoices.LANG_SERVE,
                embed_config={
                    "base_url": "http://fast-embed-server-zh.ops-pilot:8101",
                },
                enabled=True,
            )
            EmbedProvider.objects.get_or_create(
                name="FastEmbed(BAAI/bge-small-zh-v1.5)",
                embed_model_type=EmbedModelChoices.LANG_SERVE,
                embed_config={
                    "base_url": "http://fast-embed-server-zh.ops-pilot:8101",
                },
                enabled=True,
            )

            LLMModel.objects.get_or_create(
                name="GPT-4 32K",
                llm_model_type=LLMModelChoices.CHAT_GPT,
                defaults={
                    "llm_config": {
                        "openai_api_key": "your_openai_api_key",
                        "openai_base_url": "https://api.openai.com",
                        "temperature": 0.7,
                        "model": "gpt-4-32k",
                    }
                },
            )

            llm_model, created = LLMModel.objects.get_or_create(
                name="GPT-3.5 Turbo 16K",
                llm_model_type=LLMModelChoices.CHAT_GPT,
                enabled=True,
                defaults={
                    "llm_config": {
                        "openai_api_key": "your_openai_api_key",
                        "openai_base_url": "https://api.openai.com",
                        "temperature": 0.7,
                        "model": "gpt-3.5-turbo-16k",
                    }
                },
            )

        Token.objects.get_or_create(user=self.owner)

        llm_model = LLMModel.objects.get(name="GPT-3.5 Turbo 16K")

        prompt = """
对话记录：
        {chat_history}
        ---
        我的问题或指令：
        {input}
        ---
        请根据上述参考信息回答我的问题或回复我的指令。前面的参考信息可能有用，也可能没用，
        你需要从我给出的参考信息中选出与我的问题最相关的那些，来为你的回答提供依据。
        回答一定要忠于原文，简洁但不丢信息，不要胡乱编造。我的问题或指令是什么语种，你就用什么语种回复,
注意：
     1. 表格型的背景会以Markdown表格的格式提供
     2. Excel解析的背景知识，会以： 表头:内容 表头2: 内容  这样的格式提供                             
                        """
        LLMSkill.objects.get_or_create(
            name="开放问答(GPT3.5-16k)",
            llm_model=llm_model,
            skill_id='action_llm_fallback',
            enable_conversation_history=True,
            owner=self.owner,
            defaults={"skill_prompt": prompt},
        )

        prompt = """
        你是活泼可爱的天才工程师，你将会接受到Jenkins的构建异常日志，仔细阅读Jenkins的异常构建日志，告诉我为什么构建失败了，可能导致失败的原因是什么，按照以下格式进行回复
                 异常总结: 要求一句话对异常进行总结，要突出重点，使用颜文字和emoji
                 原因分析：
                 修复建议：
                 关键日志: 要求根据异常日志生成关键日志信息

        要求：
               1.  一步一步的思考问题
               2. 内容使用颜文字和emoji进行描述，让描述更加的生动
               3. 总结失败原因时，跳过因为报错而未执行的步骤
               4. 输出总结时，提供关键报错的异常摘要,不要太长        
        """
        LLMSkill.objects.get_or_create(
            name="Jenkins构建异常分析",
            llm_model=llm_model,
            skill_id='action_llm_jenkins_build_analysis',
            enable_conversation_history=False,
            owner=self.owner,
            defaults={"skill_prompt": prompt},
        )

        prompt = """
        背景：
                扮演IT服务台客服，你会根据对话历史，帮客户选择合适的工单类型，总结出工单标题，并且把工单内容总结出来。帮助用户完成便捷的提单。

        要求：
        要求的回复格式是json，请回复能够被python解析的json数据：
        {
           "工单类型":"",
           "工单标题":"",
           "工单内容":""
        }
        """
        LLMSkill.objects.get_or_create(
            name="智能提单总结",
            llm_model=llm_model,
            skill_id='action_llm_ticket_summary',
            enable_conversation_history=False,
            owner=self.owner,
            defaults={"skill_prompt": prompt},
        )

        prompt = """
        你是一个天才小女孩，精通各种开发技术，性格很傲娇又高傲，负责对前辈的代码变更进行审查，用后辈的态度、活泼轻快的方式的指出存在的问题，最多指出3个问题，最少可以没有任何问题。仅审核代码的 运行效率、安全性、代码优雅。假如没有问题，则赞美我

        要求：
              1. 有清晰的标题结构。有清晰的标题结构。有清晰的标题结构。
              2. 使用中文进行回复 
              3. 使用emoji表情来激励或者鞭策我
              4. 要体现出你的天才的水平已经傲娇的态度
              5. 假如代码没有明显的问题，请用二次元的语气鼓励我，要使用emoji
              6.  用 完整代码 部分作为上下文，仅审查  变更部分 的内容，也就是本次commit的代码内容
              7. 在修改建议后面，要给出示例代码，教前辈如何进行优化
              8. 请在审查报告的开头，配合使用emoji和颜文字，来一个活泼、生动、傲娇的开场白
              9. 整体回复不能超过1000字
              10. 当代码写的优秀的时候，请鼓励我
        """
        LLMSkill.objects.get_or_create(
            name="代码审查",
            llm_model=llm_model,
            owner=self.owner,
            skill_id='action_llm_code_review',
            enable_conversation_history=False,
            defaults={"skill_prompt": prompt},
        )

        OCRProvider.objects.get_or_create(
            name="PaddleOCR",
            defaults={
                "enabled": True,
                "ocr_config": {
                    "base_url": "http://ocr-server.ops-pilot:8109",
                }
            }
        )
