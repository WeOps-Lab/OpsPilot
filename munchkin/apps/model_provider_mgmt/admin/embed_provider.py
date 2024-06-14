from apps.model_provider_mgmt.models import EmbedProvider
from django.contrib import admin
from django.db.models import JSONField
from django_ace import AceWidget
from unfold.admin import ModelAdmin


@admin.register(EmbedProvider)
class EmbedProviderAdmin(ModelAdmin):
    list_display = ["name", "embed_model", "enabled"]
    search_fields = ["name"]
    list_filter = ["embed_model"]
    list_display_links = ["name"]
    ordering = ["id"]
    filter_horizontal = []
    fieldsets = [
        (None, {"fields": ["name", "enabled", "embed_model", "embed_config"]}),
    ]
    formfield_overrides = {JSONField: {"widget": AceWidget(mode="json", theme="chrome", width="700px")}}
