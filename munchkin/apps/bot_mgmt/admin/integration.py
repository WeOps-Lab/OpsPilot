from django.contrib import admin
from django_ace.widgets import AceWidget
from django_yaml_field.fields import YAMLField

from apps.bot_mgmt.models import Integration
from apps.core.admin.guarded_admin_base import GuardedAdminBase


@admin.register(Integration)
class IntegrationAdmin(GuardedAdminBase):
    def get_list_display(self, request):
        list_display = ['name', 'integration']
        if request.user.is_superuser:
            list_display.append("owner_name")
        return list_display

    formfield_overrides = {YAMLField: {"widget": AceWidget(mode="yaml", theme="chrome", width="700px")}}
    search_fields = ['name']
    list_filter = ['name']
    list_display_links = ['name']
    ordering = ['id']

    fieldsets = (
        (None, {
            'fields': ('name', 'integration', 'integration_config')
        }),
    )
