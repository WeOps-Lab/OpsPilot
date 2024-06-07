from django.db import models
from django_minio_backend import MinioBackend
from django_yaml_field import YAMLField

from apps.channel_mgmt.models import Channel, ChannelUserGroup, ChannelUser
from apps.model_provider_mgmt.models import LLMSkill


class ContentPack(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255, verbose_name='扩展包名称')
    description = models.TextField(verbose_name='描述', blank=True, null=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = '扩展包'
        verbose_name_plural = verbose_name


ACTION_TYPE_CHOICES = [
    ('action_llm_fallback', '开放型对话'),
    ('action_external_utter', '人工介入'),
]


class RasaModel(models.Model):
    id = models.AutoField(primary_key=True)
    content_packs = models.ManyToManyField(ContentPack, verbose_name='扩展包', null=True, blank=True)
    name = models.CharField(max_length=255, verbose_name='模型名称')
    description = models.TextField(blank=True, null=True, verbose_name='描述')
    model_file = models.FileField(verbose_name="文件",
                                  null=True,
                                  blank=True,
                                  storage=MinioBackend(bucket_name='munchkin-private'),
                                  upload_to='rasa_models')
    train_data_file = models.FileField(verbose_name="训练数据",
                                       null=True,
                                       blank=True,
                                       storage=MinioBackend(bucket_name='munchkin-private'),
                                       upload_to='rasa_train_data')
    workflow_id = models.CharField(max_length=255, verbose_name='训练任务ID', null=True, blank=True)
    pipeline_config = YAMLField(verbose_name='模型配置', default={
        "pipeline": [
            {"name": "KeywordIntentClassifier", "case_sensitive": True},
            {"name": "FallbackClassifier", "threshold": 0.7,
             "ambiguity_threshold": 0.1}
        ]})
    policies_config = YAMLField(verbose_name='策略配置', default={
        "policies": [
            {
                "name": "RulePolicy",
                "core_fallback_threshold": 0.4,
                "core_fallback_action_name": "action_llm_fallback"
            }
        ]})

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = '模型'
        verbose_name_plural = verbose_name


class BotActions(models.Model):
    id = models.AutoField(primary_key=True)
    content_pack = models.ForeignKey(ContentPack, on_delete=models.CASCADE, verbose_name='扩展包')

    name = models.CharField(max_length=255, verbose_name='动作名称', choices=ACTION_TYPE_CHOICES)
    description = models.TextField(blank=True, null=True, verbose_name='描述')

    llm_skill = models.ForeignKey(LLMSkill, on_delete=models.CASCADE, verbose_name='大模型技能', null=True, blank=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = '动作'
        verbose_name_plural = verbose_name


class RasaEntity(models.Model):
    id = models.AutoField(primary_key=True)
    content_pack = models.ForeignKey(ContentPack, on_delete=models.CASCADE, verbose_name='扩展包')
    name = models.CharField(max_length=255, verbose_name='实体名称')
    description = models.TextField(blank=True, null=True, verbose_name='描述')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = '实体'
        verbose_name_plural = verbose_name


class Intent(models.Model):
    id = models.AutoField(primary_key=True)
    content_pack = models.ForeignKey(ContentPack, on_delete=models.CASCADE, verbose_name='扩展包')
    name = models.CharField(max_length=255, verbose_name='意图名称')
    description = models.TextField(blank=True, null=True, verbose_name='描述')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = '意图'
        verbose_name_plural = verbose_name


class IntentCorpus(models.Model):
    id = models.AutoField(primary_key=True)
    intent = models.ForeignKey(Intent, on_delete=models.CASCADE, verbose_name='意图')
    corpus = models.TextField(verbose_name='语料')

    def __str__(self):
        return self.corpus

    class Meta:
        verbose_name = '意图语料'
        verbose_name_plural = verbose_name


class RasaRules(models.Model):
    id = models.AutoField(primary_key=True)
    content_pack = models.ForeignKey(ContentPack, on_delete=models.CASCADE, verbose_name='扩展包')
    name = models.CharField(max_length=255, verbose_name='规则名称')
    description = models.TextField(blank=True, null=True, verbose_name='描述')
    rule_steps = YAMLField(verbose_name='规则',
                           default={"steps": [{"intent": "intent_name"}]})

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = '规则'
        verbose_name_plural = verbose_name


class RasaStories(models.Model):
    id = models.AutoField(primary_key=True)
    content_pack = models.ForeignKey(ContentPack, on_delete=models.CASCADE, verbose_name='扩展包')
    name = models.CharField(max_length=255, verbose_name='故事名称')
    description = models.TextField(blank=True, null=True, verbose_name='描述')
    story = YAMLField(verbose_name='故事', default={
        "steps": [
            {
                "intent": "intent_name",
            }
        ],
    })

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = '故事'
        verbose_name_plural = verbose_name


class RasaResponse(models.Model):
    id = models.AutoField(primary_key=True)
    content_pack = models.ForeignKey(ContentPack, on_delete=models.CASCADE, verbose_name='扩展包')
    name = models.CharField(max_length=255, verbose_name='回复名称')
    description = models.TextField(blank=True, null=True, verbose_name='描述')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = '回复'
        verbose_name_plural = verbose_name


class RasaForms(models.Model):
    id = models.AutoField(primary_key=True)
    content_pack = models.ForeignKey(ContentPack, on_delete=models.CASCADE, verbose_name='扩展包')
    name = models.CharField(max_length=255, verbose_name='表单名称')
    description = models.TextField(blank=True, null=True, verbose_name='描述')
    form = YAMLField(verbose_name='表单', default={
        "form_name": {
            "required_slots": ["slot_name"],
        }
    })

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = '表单'
        verbose_name_plural = verbose_name


class RasaSlots(models.Model):
    id = models.AutoField(primary_key=True)
    content_pack = models.ForeignKey(ContentPack, on_delete=models.CASCADE, verbose_name='扩展包')
    name = models.CharField(max_length=255, verbose_name='槽位名称')
    description = models.TextField(blank=True, null=True, verbose_name='描述')
    slot = YAMLField(verbose_name='槽位', default={
        "slot_name": {
            "type": "text",
            "influence_conversation": True,
            "mappings": [
                {
                    "type": "custom"
                }
            ],
        }
    })

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = '槽位'
        verbose_name_plural = verbose_name


class RasaResponseCorpus(models.Model):
    id = models.AutoField(primary_key=True)
    response = models.ForeignKey(RasaResponse, on_delete=models.CASCADE, verbose_name='回复')
    corpus = models.TextField(verbose_name='语料')

    def __str__(self):
        return self.corpus

    class Meta:
        verbose_name = '回复语料'
        verbose_name_plural = verbose_name
