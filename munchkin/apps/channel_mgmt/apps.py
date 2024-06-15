from django.apps import AppConfig


class ChannelMgmtConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "apps.channel_mgmt"
    verbose_name = "通道管理"

    def ready(self):
        import apps.channel_mgmt.signals  # noqa
