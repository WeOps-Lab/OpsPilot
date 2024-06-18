from django.apps import AppConfig


class BotMgmtConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "apps.bot_mgmt"
    verbose_name = "机器人管理"

    def ready(self):
        import apps.bot_mgmt.signals  # noqa
