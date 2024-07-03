from django.contrib import admin
from django.forms import JSONField
from django.urls import reverse
from django.utils.html import format_html
from django_ace import AceWidget

from apps.core.admin.guarded_admin_base import GuardedAdminBase
from apps.knowledge_mgmt.models import FileKnowledge


@admin.register(FileKnowledge)
class FileKnowledgeAdmin(GuardedAdminBase):
    search_fields = ["knowledge_base_folder", "title"]
    list_display_links = ["title"]
    list_filter = ["knowledge_base_folder"]
    ordering = ["id"]
    filter_horizontal = []
    readonly_fields = ["title"]
    fieldsets = (
        ("", {"fields": ("knowledge_base_folder", "title", "file", "custom_metadata")}),
        ("分块解析",
         {"fields": ("enable_general_parse", ("general_parse_chunk_size", "general_parse_chunk_overlap"))}),
        ("语义分块解析",
         {"fields": ("enable_semantic_chunck_parse", "semantic_chunk_parse_embedding_model")}),
    )
    formfield_overrides = {JSONField: {"widget": AceWidget(mode="json", theme="chrome", width="700px")}}

    def get_list_display(self, request):
        list_display = ["knowledge_base_folder_link", "title", "file"]
        if request.user.is_superuser:
            list_display.append('owner_name')
        return list_display

    def knowledge_base_folder_link(self, obj):
        link = reverse("admin:knowledge_mgmt_knowledgebasefolder_change", args=[obj.knowledge_base_folder.id])
        return format_html('<a href="{}">{}</a>', link, obj.knowledge_base_folder)

    knowledge_base_folder_link.short_description = "知识库"
