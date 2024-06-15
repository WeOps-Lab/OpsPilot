from apps.contentpack_mgmt.models import ContentPack, RasaEntity
from apps.core.admin.guarded_admin_base import GuardedAdminBase
from django.contrib import admin
from django.urls import reverse
from django.utils.html import format_html
from unfold.admin import ModelAdmin


@admin.register(RasaEntity)
class RasaEntityAdmin(GuardedAdminBase):
    def get_list_display(self, request):
        list_display = ["content_pack_link", "name"]
        if request.user.is_superuser:
            list_display.append('owner_name')
        return list_display

    search_fields = ["name"]
    list_filter = ["content_pack", "name"]
    list_display_links = ["name"]
    ordering = ["id"]
    filter_horizontal = []

    fieldsets = ((None, {"fields": ("content_pack", "name", "description")}),)

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "content_pack":
            kwargs["queryset"] = ContentPack.objects.filter(owner=request.user)
        return super().formfield_for_foreignkey(db_field, request, **kwargs)

    def content_pack_link(self, obj):
        link = reverse("admin:contentpack_mgmt_contentpack_change", args=[obj.content_pack.id])
        return format_html('<a href="{}">{}</a>', link, obj.content_pack)

    content_pack_link.short_description = "扩展包"
