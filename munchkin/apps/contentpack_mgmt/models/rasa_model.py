from django.db import models
from django_minio_backend import MinioBackend
from django_yaml_field import YAMLField


class RasaModel(models.Model):
    id = models.AutoField(primary_key=True)
    content_packs = models.ManyToManyField('contentpack_mgmt.ContentPack', verbose_name='扩展包', null=True, blank=True)
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
