from apps.model_provider_mgmt.models import LLMModel
from django.contrib import admin
from django.db.models import JSONField
from django_ace import AceWidget
from unfold.admin import ModelAdmin


@admin.register(LLMModel)
class LLMModelAdmin(ModelAdmin):
    list_display = ["name", "llm_model"]
    search_fields = ["name"]
    list_filter = ["llm_model"]
    list_display_links = ["name"]

    ordering = ["id"]
    filter_horizontal = []

    formfield_overrides = {JSONField: {"widget": AceWidget(mode="json", theme="chrome", width="700px")}}

    def has_module_permission(self, request):
        return request.user.is_superuser
