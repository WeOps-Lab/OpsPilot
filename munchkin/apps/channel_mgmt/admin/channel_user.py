from apps.channel_mgmt.models import ChannelUser, ChannelUserGroup
from apps.core.admin.guarded_admin_base import GuardedAdminBase
from django.contrib import admin
from django.urls import reverse
from django.utils.html import format_html
from unfold.admin import ModelAdmin


@admin.register(ChannelUser)
class ChannelUserAdmin(GuardedAdminBase):
    search_fields = ["name"]
    list_filter = ["name"]
    list_display_links = ["channel_user_group_link", "user_id"]
    ordering = ["id"]
    filter_horizontal = []

    fieldsets = ((None, {"fields": ("channel_user_group", "user_id", "name")}),)

    def get_list_display(self, request):
        list_display = ["channel_user_group", "user_id", "name"]
        if request.user.is_superuser:
            list_display.append('owner_name')
        return list_display

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "channel_user_group":
            kwargs["queryset"] = ChannelUserGroup.objects.filter(owner=request.user)
        return super().formfield_for_foreignkey(db_field, request, **kwargs)

    def channel_user_group_link(self, obj):
        link = reverse("admin:channel_mgmt_channelusergroup_change", args=[obj.channel_user_group.id])
        return format_html('<a href="{}">{}</a>', link, obj.channel_user_group)

    channel_user_group_link.short_description = "用户组"
