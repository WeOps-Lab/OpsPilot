from django.contrib import admin
from django.db.models import JSONField
from django_ace import AceWidget
from unfold.admin import ModelAdmin

from apps.model_provider_mgmt.models import RerankProvider


@admin.register(RerankProvider)
class RerankProviderAdmin(ModelAdmin):
    list_display = ['name', 'rerank_model', 'enabled']
    search_fields = ['name']
    list_filter = ['rerank_model']
    list_display_links = ['name']
    ordering = ['id']
    filter_horizontal = []
    fieldsets = (
        (None, {
            'fields': ('name', 'rerank_model', 'enabled', 'rerank_config')
        }),
    )
    formfield_overrides = {
        JSONField: {
            "widget": AceWidget(mode="json", theme='chrome', width='700px')
        }
    }
