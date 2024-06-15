from apps.bot_mgmt.models import Bot, BotConversationHistory
from apps.channel_mgmt.models import ChannelUser
from apps.core.admin.guarded_admin_base import GuardedAdminBase
from django.contrib import admin
from django.urls import reverse
from django.utils.html import format_html
from unfold.admin import ModelAdmin


@admin.register(BotConversationHistory)
class BotConversationHistoryAdmin(GuardedAdminBase):
    def get_list_display(self, request):
        list_display = ["bot", "channel_link", "user_link", "conversation_role", "short_conversation", "created_at"]
        if request.user.is_superuser:
            list_display.append("owner_name")
        return list_display

    search_fields = ["conversation"]
    list_filter = ["bot", "user", "conversation_role", "created_at"]
    list_display_links = ["short_conversation"]
    ordering = ["-created_at"]
    filter_horizontal = []

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "user":
            kwargs["queryset"] = ChannelUser.objects.filter(owner=request.user)
        elif db_field.name == "bot":
            kwargs["queryset"] = Bot.objects.filter(owner=request.user)
        return super().formfield_for_foreignkey(db_field, request, **kwargs)

    fieldsets = (
        (
            None,
            {
                "fields": (
                    "bot",
                    "user",
                    "conversation_role",
                    "conversation",
                )
            },
        ),
    )

    def user_link(self, obj):
        link = reverse("admin:channel_mgmt_channeluser_change", args=[obj.user.id])
        return format_html('<a href="{}">{}</a>', link, obj.user)

    user_link.short_description = "用户"

    def channel_link(self, obj):
        link = reverse("admin:channel_mgmt_channel_change", args=[obj.user.channel_user_group.channel.id])
        return format_html('<a href="{}">{}</a>', link, obj.user.channel_user_group.channel.name)

    channel_link.short_description = "通道"

    def short_conversation(self, obj):
        if len(obj.conversation) > 30:
            return f"{obj.conversation[:30]}..."
        else:
            return obj.conversation

    short_conversation.short_description = "对话内容"
