from django.contrib import admin
from unfold.admin import ModelAdmin

from apps.channel_mgmt.models import ChannelUserGroup


@admin.register(ChannelUserGroup)
class ChannelUserGroupAdmin(ModelAdmin):
    list_display = ['channel', 'name']
    search_fields = ['name']
    list_filter = ['name']
    list_display_links = ['name']
    ordering = ['id']
    filter_horizontal = []
