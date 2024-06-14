from apps.channel_mgmt.models import Channel
from django.contrib import admin
from django_ace import AceWidget
from django_yaml_field import YAMLField
from unfold.admin import ModelAdmin


@admin.register(Channel)
class ChannelAdmin(ModelAdmin):
    list_display = ["channel_type", "name"]
    search_fields = ["name"]
    list_filter = ["channel_type", "name"]
    list_display_links = ["name"]
    ordering = ["id"]
    filter_horizontal = []

    formfield_overrides = {YAMLField: {"widget": AceWidget(mode="yaml", theme="chrome", width="700px")}}
