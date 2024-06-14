from django.contrib import admin
from django.urls import reverse
from django.utils.html import format_html
from unfold.admin import ModelAdmin

from apps.contentpack_mgmt.models import IntentCorpus
from apps.core.admin.guarded_admin_base import GuardedAdminBase


@admin.register(IntentCorpus)
class IntentCorpusAdmin(GuardedAdminBase):
    list_display = ['content_pack_link', 'intent_link', 'corpus']
    search_fields = ['corpus']
    list_filter = ['intent']
    list_display_links = ['corpus']
    ordering = ['id']
    filter_horizontal = []

    def content_pack_link(self, obj):
        link = reverse("admin:contentpack_mgmt_contentpack_change", args=[obj.intent.content_pack.id])
        return format_html('<a href="{}">{}</a>', link, obj.intent.content_pack)

    content_pack_link.short_description = '扩展包'

    def intent_link(self, obj):
        link = reverse("admin:contentpack_mgmt_intent_change", args=[obj.intent.id])
        return format_html('<a href="{}">{}</a>', link, obj.intent)

    intent_link.short_description = '意图'
