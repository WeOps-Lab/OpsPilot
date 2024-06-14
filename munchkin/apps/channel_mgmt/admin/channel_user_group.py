from apps.channel_mgmt.models import Channel, ChannelUserGroup
from apps.core.admin.guarded_admin_base import GuardedAdminBase
from django.contrib import admin
from unfold.admin import ModelAdmin


@admin.register(ChannelUserGroup)
class ChannelUserGroupAdmin(GuardedAdminBase):
    list_display = ["channel", "name"]
    search_fields = ["name"]
    list_filter = ["name"]
    list_display_links = ["name"]
    ordering = ["id"]
    filter_horizontal = []

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "channel":
            kwargs["queryset"] = Channel.objects.filter(owner=request.user)
        return super().formfield_for_foreignkey(db_field, request, **kwargs)

    fieldsets = ((None, {"fields": ("channel", "name")}),)
