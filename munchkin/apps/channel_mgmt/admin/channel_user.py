from django.contrib import admin
from django.urls import reverse
from django.utils.html import format_html
from unfold.admin import ModelAdmin

from apps.channel_mgmt.models import ChannelUser


@admin.register(ChannelUser)
class ChannelUserAdmin(ModelAdmin):
    list_display = ['channel_user_group_link', 'user_id', 'name']
    search_fields = ['name']
    list_filter = ['name']
    list_display_links = ['channel_user_group_link', 'user_id']
    ordering = ['id']
    filter_horizontal = []

    def channel_user_group_link(self, obj):
        link = reverse("admin:channel_mgmt_channelusergroup_change", args=[obj.channel_user_group.id])
        return format_html('<a href="{}">{}</a>', link, obj.channel_user_group)

    channel_user_group_link.short_description = '用户组'
