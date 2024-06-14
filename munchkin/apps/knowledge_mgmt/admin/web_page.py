from apps.core.admin.guarded_admin_base import GuardedAdminBase
from apps.knowledge_mgmt.models import WebPageKnowledge
from django.contrib import admin
from django.forms import JSONField
from django.urls import reverse
from django.utils.html import format_html
from django_ace import AceWidget
from unfold.admin import ModelAdmin


@admin.register(WebPageKnowledge)
class WebPageKnowledgeAdmin(GuardedAdminBase):
    list_display = ["knowledge_base_folder_link", "title", "url", "max_depth"]
    search_fields = ["knowledge_base_folder", "title"]
    list_display_links = ["title"]
    list_filter = ["knowledge_base_folder"]
    ordering = ["id"]
    filter_horizontal = []
    fieldsets = (("", {"fields": ("knowledge_base_folder", "title", "url", "max_depth", "custom_metadata")}),)

    formfield_overrides = {JSONField: {"widget": AceWidget(mode="json", theme="chrome", width="700px")}}

    def knowledge_base_folder_link(self, obj):
        link = reverse("admin:knowledge_mgmt_knowledgebasefolder_change", args=[obj.knowledge_base_folder.id])
        return format_html('<a href="{}">{}</a>', link, obj.knowledge_base_folder)

    knowledge_base_folder_link.short_description = "知识库"
