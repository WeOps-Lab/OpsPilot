from apps.bot_mgmt.models import BotSkillRule
from django.contrib import admin
from unfold.admin import ModelAdmin


@admin.register(BotSkillRule)
class BotActionRuleAdmin(ModelAdmin):
    list_display = ["name", "bot_id", "skill", "channel"]
    search_fields = ["name"]
    list_filter = ["name"]
    list_display_links = ["name"]
    ordering = ["id"]
    filter_horizontal = ["rule_user_groups", "rule_user"]
