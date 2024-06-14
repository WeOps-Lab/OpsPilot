from apps.contentpack_mgmt.models import ContentPack, Intent, IntentCorpus
from apps.core.admin.guarded_admin_base import GuardedAdminBase
from django.contrib import admin
from django.urls import reverse
from django.utils.html import format_html
from unfold.admin import ModelAdmin


class IntentCorpusInline(admin.StackedInline):
    model = IntentCorpus
    show_change_link = True
    extra = 0
    fieldsets = ((None, {"fields": ("corpus",)}),)


@admin.register(Intent)
class IntentAdmin(GuardedAdminBase):
    list_display = ["content_pack_link", "name"]
    search_fields = ["name"]
    list_filter = ["content_pack", "name"]
    list_display_links = ["name"]
    ordering = ["id"]
    filter_horizontal = []
    inlines = [IntentCorpusInline]

    fieldsets = (("基本信息", {"fields": ["content_pack", "name", "description"]}),)

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "content_pack":
            kwargs["queryset"] = ContentPack.objects.filter(owner=request.user)
        return super().formfield_for_foreignkey(db_field, request, **kwargs)

    def content_pack_link(self, obj):
        link = reverse("admin:contentpack_mgmt_contentpack_change", args=[obj.content_pack.id])
        return format_html('<a href="{}">{}</a>', link, obj.content_pack)

    content_pack_link.short_description = "扩展包"
