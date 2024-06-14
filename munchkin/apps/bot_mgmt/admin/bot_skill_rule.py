from django.contrib import admin
from unfold.admin import ModelAdmin

from apps.bot_mgmt.models import BotSkillRule, Bot
from apps.channel_mgmt.models import ChannelUserGroup, ChannelUser
from apps.core.admin.guarded_admin_base import GuardedAdminBase
from apps.model_provider_mgmt.models import LLMSkill


@admin.register(BotSkillRule)
class BotSkillRuleAdmin(GuardedAdminBase):
    list_display = ['name', 'bot_id', 'skill', 'channel']
    search_fields = ['name']
    list_filter = ['name']
    list_display_links = ['name']
    ordering = ['id']
    filter_horizontal = ['rule_user_groups', 'rule_user']

    fieldsets = (
        (None, {
            'fields': ('name', 'bot_id', 'skill', 'channel', 'rule_user_groups', 'rule_user')
        }),
    )

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "bot_id":
            kwargs["queryset"] = Bot.objects.filter(owner=request.user)
        elif db_field.name == "skill":
            kwargs["queryset"] = LLMSkill.objects.filter(owner=request.user)
        return super().formfield_for_foreignkey(db_field, request, **kwargs)

    def formfield_for_manytomany(self, db_field, request, **kwargs):
        if db_field.name == "rule_user_groups":
            kwargs["queryset"] = ChannelUserGroup.objects.filter(owner=request.user)
        elif db_field.name == "rule_user":
            kwargs["queryset"] = ChannelUser.objects.filter(owner=request.user)
        return super().formfield_for_manytomany(db_field, request, **kwargs)
