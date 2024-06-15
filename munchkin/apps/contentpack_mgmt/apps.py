from django.apps import AppConfig


class ContentpackMgmtConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "apps.contentpack_mgmt"
    verbose_name = "扩展包管理"

    def ready(self):
        import apps.contentpack_mgmt.signals  # noqa
