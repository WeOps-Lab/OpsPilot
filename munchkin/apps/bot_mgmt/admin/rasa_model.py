from django.contrib import admin

from apps.bot_mgmt.models import RasaModel
from apps.core.admin.guarded_admin_base import GuardedAdminBase


@admin.register(RasaModel)
class RasaModelAdmin(GuardedAdminBase):
    def get_list_display(self, request):
        list_display = ["name", "model_file", "description"]
        if request.user.is_superuser:
            list_display.append('owner_name')
        return list_display

    search_fields = ["name"]
    list_filter = ["name"]
    list_display_links = ["name"]
    ordering = ["id"]

    fieldsets = (
        (None, {"fields": ("name", 'model_file', "description")}),
    )
