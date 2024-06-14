from django.contrib import admin
from django_ace import AceWidget
from django_yaml_field import YAMLField
from unfold.admin import ModelAdmin

from apps.channel_mgmt.models import Channel
from apps.core.admin.guarded_admin_base import GuardedAdminBase


@admin.register(Channel)
class ChannelAdmin(GuardedAdminBase):
    list_display = ['channel_type', 'name']
    search_fields = ['name']
    list_filter = ['channel_type', 'name']
    list_display_links = ['name']
    ordering = ['id']
    filter_horizontal = []

    fieldsets = (
        (None, {
            'fields': ('name', 'channel_type', 'channel_config')
        }),
    )
    formfield_overrides = {YAMLField: {
        "widget": AceWidget(mode="yaml", theme='chrome', width='700px')}
    }
