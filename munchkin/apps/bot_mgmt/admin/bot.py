from django.contrib import admin, messages
from django.http import HttpRequest
from django.shortcuts import redirect
from django.urls import reverse
from django.utils.html import format_html
from unfold.decorators import action

from apps.bot_mgmt.models import Bot, RasaModel, AutomationSkill, Integration
from apps.channel_mgmt.models import Channel
from apps.core.admin.guarded_admin_base import GuardedAdminBase
from apps.core.utils.kubernetes_client import KubernetesClient
from apps.model_provider_mgmt.models import LLMSkill


@admin.register(Bot)
class BotAdmin(GuardedAdminBase):
    def get_list_display(self, request):
        list_display = [
            "name",
            "assistant_id",
            "rasa_model_link",
            "channels_link",
            "online",
            "enable_bot_domain",
            "bot_domain",
            "enable_ssl",
            "enable_node_port",
            "node_port",
        ]
        if request.user.is_superuser:
            list_display.append("owner_name")
        return list_display

    search_fields = ["name"]
    list_filter = ["name"]
    list_display_links = ["name", "rasa_model_link", "channels_link"]
    ordering = ["id"]
    actions = ["start_pilot", "stop_pilot"]
    filter_horizontal = ["channels", "llm_skills", "integration"]
    fieldsets = (
        ("基本信息", {"fields": ("name", "assistant_id", "description")}),
        ("模型设置", {"fields": ("rasa_model",)}),
        ("集成", {"fields": ("integration",)}),
        ("LLM技能", {"fields": ("llm_skills",)}),
        ("通道", {"fields": ("channels",)}),
        (
            "高级设置",
            {
                "fields": (
                "enable_bot_domain", "enable_ssl", "bot_domain", "enable_node_port", "node_port", "node_selector"),
            },
        ),
    )

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "rasa_model":
            kwargs["queryset"] = RasaModel.objects.filter(owner=request.user)
        return super().formfield_for_foreignkey(db_field, request, **kwargs)

    def formfield_for_manytomany(self, db_field, request, **kwargs):
        if db_field.name == "channels":
            kwargs["queryset"] = Channel.objects.filter(owner=request.user)
        elif db_field.name == "llm_skills":
            kwargs["queryset"] = LLMSkill.objects.filter(owner=request.user)
        elif db_field.name == "integration":
            kwargs["queryset"] = Integration.objects.filter(owner=request.user)
        return super().formfield_for_manytomany(db_field, request, **kwargs)

    def channels_link(self, obj):
        links = []
        for channel in obj.channels.all():
            url = reverse("admin:channel_mgmt_channel_change", args=[channel.id])
            links.append(format_html('<a href="{}">{}</a>', url, channel))
        return format_html(",".join(links))

    channels_link.short_description = "通道"

    def rasa_model_link(self, obj):
        if obj.rasa_model is None:
            return "-"

        link = reverse("admin:bot_mgmt_rasamodel_change", args=[obj.rasa_model.id])
        return format_html('<a href="{}">{}</a>', link, obj.rasa_model)

    rasa_model_link.short_description = "模型"

    @action(description="上线", url_path="start_pilot")
    def start_pilot(self, request: HttpRequest, bots):
        client = KubernetesClient()
        for bot in bots:
            client.start_pilot(bot)
            bot.online = True
            bot.save()
        messages.success(request, "机器人上线")
        return redirect(reverse("admin:bot_mgmt_bot_changelist"))

    @action(description="下线", url_path="stop_pilot")
    def stop_pilot(self, request: HttpRequest, bots):
        client = KubernetesClient()
        for bot in bots:
            client.stop_pilot(bot.id)
            bot.online = False
            bot.save()
        messages.success(request, "机器人下线")
        return redirect(reverse("admin:bot_mgmt_bot_changelist"))
