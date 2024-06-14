from django.contrib import admin, messages
from django.http import HttpRequest
from django.shortcuts import redirect
from django.urls import reverse
from django_ace import AceWidget
from django_yaml_field import YAMLField
from unfold.admin import ModelAdmin
from unfold.decorators import action

from apps.contentpack_mgmt.models import RasaModel
from apps.contentpack_mgmt.tasks.build_rasa_train_data import build_rasa_train_data
from apps.core.admin.guarded_admin_base import GuardedAdminBase
from apps.core.utils.kubernetes_client import KubernetesClient


@admin.register(RasaModel)
class RasaModelAdmin(GuardedAdminBase):
    list_display = ['name', 'train_data_file', 'model_file', 'description']
    search_fields = ['name']
    list_filter = ['name']
    list_display_links = ['name']
    ordering = ['id']
    filter_horizontal = ['content_packs']
    formfield_overrides = {YAMLField: {
        "widget": AceWidget(mode="yaml", theme='chrome', width='700px')}
    }
    actions_row = ['build_train_data', 'train_pilot']

    fieldsets = (
        (None, {
            'fields': ('name', 'description', 'content_packs')
        }),
        ('配置', {
            'fields': ('pipeline_config', 'policies_config')
        }),
        ('模型', {
            'fields': ('model_file', 'train_data_file')
        }),
    )

    @action(description='构建语料', url_path="build_train_data")
    def build_train_data(self, request: HttpRequest, object_id: int):
        build_rasa_train_data.delay(object_id)
        messages.success(request, '开始生成语料')
        return redirect(reverse('admin:contentpack_mgmt_rasamodel_changelist'))

    @action(description='训练模型', url_path="train_pilot")
    def train_pilot(self, request: HttpRequest, object_id: int):
        client = KubernetesClient('argo')

        workflow_id = client.train_pilot(object_id)
        model = RasaModel.objects.get(id=object_id)
        model.workflow_id = workflow_id
        model.save()

        messages.success(request, '开始训练')
        return redirect(reverse('admin:contentpack_mgmt_rasamodel_changelist'))
