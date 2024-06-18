from django.contrib.auth.models import User, Permission
from django.db.models.signals import post_save
from django.dispatch import receiver


@receiver(post_save, sender=User)
def user_create_signal(sender, instance, created, **kwargs):
    if created and instance.username != 'AnonymousUser':
        # 初始化用户权限
        included_code = [
            "bot",
            "botskillrule",
            "botconversationhistory",
            "llmskill",
            "channel",
            "channelusergroup",
            "channeluser",
            "knowledgebasefolder",
            "fileknowledge",
            "manualknowledge",
            "webpageknowledge",
            "rasamodel",
        ]
        all_permission = []
        for code in included_code:
            permissions = Permission.objects.filter(codename__contains=code)
            all_permission.extend(permissions)
        instance.user_permissions.add(*all_permission)
