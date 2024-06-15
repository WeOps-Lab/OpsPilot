from apps.contentpack_mgmt.models import RasaResponseCorpus
from apps.core.admin.guarded_admin_base import GuardedAdminBase
from django.contrib import admin
from unfold.admin import ModelAdmin


@admin.register(RasaResponseCorpus)
class RasaResponseCorpusAdmin(GuardedAdminBase):
    def get_list_display(self, request):
        list_display = ["response", "corpus"]
        if request.user.is_superuser:
            list_display.append('owner_name')
        return list_display

    search_fields = ["corpus"]
    list_filter = ["response"]
    list_display_links = ["corpus"]
    ordering = ["id"]
    filter_horizontal = []
