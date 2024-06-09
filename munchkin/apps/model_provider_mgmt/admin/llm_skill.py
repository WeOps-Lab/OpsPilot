from django.contrib import admin
from django.db.models import JSONField
from django.urls import reverse
from django.utils.html import format_html
from django_ace import AceWidget
from unfold.admin import ModelAdmin

from apps.model_provider_mgmt.models import LLMSkill


@admin.register(LLMSkill)
class LLMSkillAdmin(ModelAdmin):
    list_display = ['name', 'llm_model_link', 'enable_conversation_history', 'enable_rag']
    search_fields = ['name']
    list_filter = ['llm_model', 'enable_conversation_history', 'enable_rag']
    list_display_links = ['name']

    ordering = ['id']
    filter_horizontal = ['knowledge_base_folders']

    formfield_overrides = {
        JSONField: {
            "widget": AceWidget(mode="json", theme='chrome', width='700px')
        }
    }

    def llm_model_link(self, obj):
        link = reverse("admin:model_provider_mgmt_llmmodel_change", args=[obj.llm_model.id])
        return format_html('<a href="{}">{}</a>', link, obj.llm_model)

    llm_model_link.short_description = 'LLM模型'
