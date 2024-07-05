from django.contrib import admin, messages

from apps.bot_mgmt.models import Bot
from apps.bot_mgmt.models.integrations import Integrations
from apps.core.admin.guarded_admin_base import GuardedAdminBase


@admin.register(Integrations)
class IntegrationsAdmin(GuardedAdminBase):
    def get_list_display(self, request):
        list_display = [
            "name",
            "integration_type",
            "description",
            "bot_id",
        ]
        return list_display

    search_fields = ["name"]
    list_filter = ["name"]
    list_display_links = ["name"]
    ordering = ["id"]
    fieldsets = (
        ("基本信息", {"fields": ("name", "integration_type", "description", "config", "bot_id")}),
    )

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "bot_id":
            kwargs["queryset"] = Bot.objects.filter(owner=request.user)
        return super().formfield_for_foreignkey(db_field, request, **kwargs)
