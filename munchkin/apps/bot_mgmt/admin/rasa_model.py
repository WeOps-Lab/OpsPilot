from django.contrib import admin, messages
from django.http import HttpRequest
from django.shortcuts import redirect
from django.urls import reverse
from django_ace import AceWidget
from django_yaml_field import YAMLField
from unfold.decorators import action

from apps.bot_mgmt.models import RasaModel
from apps.contentpack_mgmt.tasks.build_rasa_train_data import build_rasa_train_data
from apps.core.admin.guarded_admin_base import GuardedAdminBase
from apps.core.utils.kubernetes_client import KubernetesClient


@admin.register(RasaModel)
class RasaModelAdmin(GuardedAdminBase):
    def get_list_display(self, request):
        list_display = ["name", "model_file", "description"]
        if request.user.is_superuser:
            list_display.append('owner_name')
        return list_display

    search_fields = ["name"]
    list_filter = ["name"]
    list_display_links = ["name"]
    ordering = ["id"]

    fieldsets = (
        (None, {"fields": ("name", "description", "content_packs")}),
    )
