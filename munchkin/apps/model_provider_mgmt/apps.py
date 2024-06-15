from django.apps import AppConfig


class EmbedMgmtConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "apps.model_provider_mgmt"
    verbose_name = "模型供应商"

    def ready(self):
        import apps.model_provider_mgmt.signals  # noqa
