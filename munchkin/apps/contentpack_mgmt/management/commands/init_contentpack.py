from django.core.management import BaseCommand

from apps.channel_mgmt.models import Channel, CHANNEL_CHOICES
from apps.contentpack_mgmt.models import ContentPack, RasaModel, BotActions, BotActionRule, RasaEntity, Intent, \
    IntentCorpus, RasaRules
from apps.model_provider_mgmt.models import LLMModel, LLMModelChoices


class Command(BaseCommand):
    help = '初始化'

    def handle(self, *args, **options):
        content_pack = ContentPack.objects.create(name='核心扩展包', description='核心扩展包')

        policies_config = """
        
        """

        rasa_model = RasaModel.objects.create(name='核心模型', description='核心模型',
                                              pipeline_config={"pipeline": [
                                                  {"name": "KeywordIntentClassifier", "case_sensitive": True},
                                                  {"name": "FallbackClassifier", "threshold": 0.7,
                                                   "ambiguity_threshold": 0.1}
                                              ]},
                                              policies_config={"policies": [
                                                  {
                                                      "name": "RulePolicy",
                                                      "core_fallback_threshold": 0.4,
                                                      "core_fallback_action_name": "action_llm_fallback"
                                                  }
                                              ]})
        rasa_model.content_packs.add(content_pack)
        rasa_model.save()

        action_llm_fallback_action = BotActions.objects.create(content_pack=content_pack,
                                                               name='action_llm_fallback',
                                                               description='开放型对话')

        action_external_utter_action = BotActions.objects.create(content_pack=content_pack,
                                                                 name='action_external_utter',
                                                                 description='人工介入')

        RasaEntity.objects.create(name='content', description='人工介入回复内容', content_pack=content_pack)

        Intent.objects.create(name='out_of_scope', description='大模型回复', content_pack=content_pack)
        Intent.objects.create(name='EXTERNAL_UTTER', description='人工回复', content_pack=content_pack)

        out_of_scope_corpus = [
            '今天天气怎么样', '总结', '总结上述内容', '总结一下',
            '总结一下上述内容', '总结一下上述对话', '这个功能怎么用', 'WeOps支持哪些功能',
            '马斯克有没去参加笼中决斗', '产品对比', '你真好', '再说吧', 'jenkins是什么',
            '那你从那里获取到jenkins的相关信息的', '使用Java编写一个爬虫示例程序', '修复一个bug',
            '我要申请笔记本', '帮我查一下这个服务器的信息', '申请一下仓库权限'
        ]
        for corpus in out_of_scope_corpus:
            IntentCorpus.objects.create(intent=Intent.objects.get(name='out_of_scope'), corpus=corpus)

        RasaRules.objects.create(
            content_pack=content_pack,
            name='主动回复',
            rule_steps={"steps": [{"intent": "EXTERNAL_UTTER"}, {"action": "action_external_utter"}]})

        RasaRules.objects.create(
            content_pack=content_pack,
            name='Fallback',
            rule_steps={"steps": [{"intent": "nlu_fallback"}, {"action": "action_llm_fallback"}]})

        RasaRules.objects.create(
            content_pack=content_pack,
            name='out_of_scope',
            rule_steps={"steps": [{"intent": "out_of_scope"}, {"action": "action_llm_fallback"}]})
