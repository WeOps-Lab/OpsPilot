from django.contrib import admin
from django.db.models import TextField
from django.forms import JSONField
from django.urls import reverse
from django.utils.html import format_html
from django_ace import AceWidget
from unfold.admin import ModelAdmin
from unfold.contrib.forms.widgets import WysiwygWidget

from apps.knowledge_mgmt.models import ManualKnowledge


@admin.register(ManualKnowledge)
class ManualKnowledgeAdmin(ModelAdmin):
    list_display = ['title', 'knowledge_base_folder_link']
    search_fields = ['title']
    list_display_links = ['title']
    list_filter = ['knowledge_base_folder']
    ordering = ['id']
    filter_horizontal = []
    fieldsets = (
        ('', {
            'fields': ('knowledge_base_folder', 'title', 'content', 'custom_metadata')
        }),
    )
    formfield_overrides = {
        TextField: {
            "widget": WysiwygWidget,
        },
        JSONField: {
            "widget": AceWidget(mode="json", theme='chrome', width='700px')
        }
    }

    def knowledge_base_folder_link(self, obj):
        link = reverse("admin:knowledge_mgmt_knowledgebasefolder_change", args=[obj.knowledge_base_folder.id])
        return format_html('<a href="{}">{}</a>', link, obj.knowledge_base_folder)

    knowledge_base_folder_link.short_description = '知识库'
