from django.core.management import BaseCommand

from apps.contentpack_mgmt.models import ContentPack, RasaModel, BotActions, RasaEntity, Intent, \
    IntentCorpus, RasaRules
from apps.model_provider_mgmt.models import LLMSkill


class Command(BaseCommand):
    help = '初始化'

    def handle(self, *args, **options):
        content_pack, created = ContentPack.objects.get_or_create(name='核心扩展包', description='核心扩展包')

        rasa_model, created = RasaModel.objects.get_or_create(name='核心模型', description='核心模型')
        if created:
            rasa_model.pipeline_config = {"pipeline": [
                {
                    "name": "KeywordIntentClassifier",
                    "case_sensitive": True
                },
                {
                    "name": "FallbackClassifier", "threshold": 0.7,
                    "ambiguity_threshold": 0.1
                }
            ]}
            rasa_model.policies_config = {"policies": [
                {
                    "name": "RulePolicy",
                    "core_fallback_threshold": 0.4,
                    "core_fallback_action_name": "action_llm_fallback"
                }
            ]}
            rasa_model.content_packs.add(content_pack)
            rasa_model.save()

        BotActions.objects.get_or_create(content_pack=content_pack,
                                         name='action_llm_fallback',
                                         description='开放型对话')

        BotActions.objects.get_or_create(content_pack=content_pack,
                                         name='action_external_utter',
                                         description='人工介入')

        RasaEntity.objects.get_or_create(name='content', description='人工介入回复内容', content_pack=content_pack)

        Intent.objects.get_or_create(name='out_of_scope', description='大模型回复', content_pack=content_pack)
        Intent.objects.get_or_create(name='EXTERNAL_UTTER', description='人工回复', content_pack=content_pack)

        out_of_scope_corpus = [
            '今天天气怎么样', '总结', '总结上述内容', '总结一下',
            '总结一下上述内容', '总结一下上述对话', '这个功能怎么用', 'WeOps支持哪些功能',
            '马斯克有没去参加笼中决斗', '产品对比', '你真好', '再说吧', 'jenkins是什么',
            '那你从那里获取到jenkins的相关信息的', '使用Java编写一个爬虫示例程序', '修复一个bug',
            '我要申请笔记本', '帮我查一下这个服务器的信息', '申请一下仓库权限'
        ]
        for corpus in out_of_scope_corpus:
            IntentCorpus.objects.get_or_create(intent=Intent.objects.get(name='out_of_scope'), corpus=corpus)

        entity, created = RasaRules.objects.get_or_create(
            content_pack=content_pack,
            name='主动回复')
        if created:
            entity.rule_steps = {
                "steps": [
                    {"intent": "EXTERNAL_UTTER"}, {"action": "action_external_utter"}
                ]
            }
            entity.save()

        entity, created = RasaRules.objects.get_or_create(
            content_pack=content_pack,
            name='Fallback')
        if created:
            entity.rule_steps = {
                "steps": [
                    {"intent": "nlu_fallback"},
                    {"action": "action_llm_fallback"}
                ]}
            entity.save()

        entity, created = RasaRules.objects.get_or_create(
            content_pack=content_pack,
            name='out_of_scope')
        if created:
            entity.rule_steps = {
                "steps": [
                    {"intent": "out_of_scope"},
                    {"action": "action_llm_fallback"}
                ]
            }
            entity.save()
