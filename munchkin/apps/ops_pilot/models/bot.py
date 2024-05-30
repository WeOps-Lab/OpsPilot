from django.db import models


class Bot(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255, unique=True, verbose_name='机器人名称')
    description = models.TextField(verbose_name='机器人描述')
    is_active = models.BooleanField(default=True, verbose_name='是否启用')

    rules = models.ManyToManyField('Rules', verbose_name='规则', blank=True)
    stories = models.ManyToManyField('Stories', verbose_name='故事', blank=True)
    
    session_expiration_time = models.IntegerField(default=60, verbose_name='会话过期时间')
    carry_over_slots_to_new_session = models.BooleanField(default=True, verbose_name='是否携带槽位到新会话')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "机器人"
        verbose_name_plural = verbose_name
