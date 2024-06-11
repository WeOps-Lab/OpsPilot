from django.contrib import admin, messages
from django.http import HttpRequest
from django.shortcuts import redirect
from django.urls import reverse
from django.utils.html import format_html
from unfold.admin import ModelAdmin
from unfold.decorators import action

from apps.bot_mgmt.models import Bot
from apps.core.utils.kubernetes_client import KubernetesClient


@admin.register(Bot)
class BotAdmin(ModelAdmin):
    list_display = ['name', 'assistant_id', 'rasa_model_link', 'channels_link', 'online', 'enable_bot_domain',
                    'bot_domain',
                    'enable_ssl',
                    'enable_node_port', 'node_port']
    search_fields = ['name']
    list_filter = ['name']
    list_display_links = ['name', 'rasa_model_link', 'channels_link']
    ordering = ['id']
    actions_row = ['start_pilot', 'stop_pilot']
    filter_horizontal = ['channels', 'llm_skills']
    fieldsets = (
        ('基本信息', {
            'fields': ('name', 'assistant_id', 'description')
        }),
        ('模型设置', {
            'fields': ('rasa_model',)
        }),
        ('LLM技能', {
            'fields': ('llm_skills',)
        }),
        ('通道', {
            'fields': ('channels',)
        }), ('高级设置', {
            'fields': ('enable_bot_domain', 'enable_ssl', 'bot_domain', 'enable_node_port', 'node_port'),
        })
    )

    def channels_link(self, obj):
        links = []
        for channel in obj.channels.all():
            url = reverse("admin:channel_mgmt_channel_change", args=[channel.id])
            links.append(format_html('<a href="{}">{}</a>', url, channel))
        return format_html(','.join(links))

    channels_link.short_description = '通道'

    def rasa_model_link(self, obj):
        link = reverse("admin:contentpack_mgmt_rasamodel_change", args=[obj.rasa_model.id])
        return format_html('<a href="{}">{}</a>', link, obj.rasa_model)

    rasa_model_link.short_description = '模型'

    @action(description='上线', url_path="start_pilot")
    def start_pilot(self, request: HttpRequest, object_id: int):
        client = KubernetesClient('argo')
        bot = Bot.objects.get(id=object_id)
        client.start_pilot(bot)
        bot.online = True
        bot.save()
        messages.success(request, '机器人上线')
        return redirect(reverse('admin:bot_mgmt_bot_changelist'))

    @action(description='下线', url_path="stop_pilot")
    def stop_pilot(self, request: HttpRequest, object_id: int):
        client = KubernetesClient('argo')
        client.stop_pilot(object_id)
        bot = Bot.objects.get(id=object_id)
        bot.online = False
        bot.save()
        messages.success(request, '机器人下线')
        return redirect(reverse('admin:bot_mgmt_bot_changelist'))
