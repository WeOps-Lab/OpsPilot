from django.contrib import admin
from django.urls import reverse
from django.utils.html import format_html
from unfold.admin import ModelAdmin

from apps.bot_mgmt.models import BotConversationHistory


@admin.register(BotConversationHistory)
class BotConversationHistoryAdmin(ModelAdmin):
    list_display = ['bot', 'channel_link', 'user_link', 'conversation_role', 'short_conversation', 'created_at']
    search_fields = ['conversation']
    list_filter = ['bot', 'user', 'conversation_role', 'created_at']
    list_display_links = ['short_conversation']
    ordering = ['-created_at']
    filter_horizontal = []

    def user_link(self, obj):
        link = reverse("admin:channel_mgmt_channeluser_change", args=[obj.user.id])
        return format_html('<a href="{}">{}</a>', link, obj.user)

    user_link.short_description = '用户'

    def channel_link(self, obj):
        link = reverse("admin:channel_mgmt_channel_change", args=[obj.user.channel_user_group.channel.id])
        return format_html('<a href="{}">{}</a>', link, obj.user.channel_user_group.channel.name)

    channel_link.short_description = '通道'

    def short_conversation(self, obj):
        if len(obj.conversation) > 30:
            return f'{obj.conversation[:30]}...'
        else:
            return obj.conversation

    short_conversation.short_description = '对话内容'
