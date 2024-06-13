import json
import logging

from django import forms
from import_export.forms import ImportForm, ConfirmImportForm
from import_export import resources
from apps.knowledge_mgmt.models import ManualKnowledge, KnowledgeBaseFolder


class ManualKnowledgeImportForm(ImportForm):
    knowledge_base_folder = forms.ModelChoiceField(queryset=KnowledgeBaseFolder.objects.all(), required=True, label="请选择需要导入的知识库")


class ManualKnowledgeConfirmImportForm(ConfirmImportForm):
    knowledge_base_folder = forms.ModelChoiceField(queryset=KnowledgeBaseFolder.objects.all(), required=True)


class ManualKnowledgeResource(resources.ModelResource):

    class Meta:
        model = ManualKnowledge
        import_id_fields = ('title',)
        fields = ('title', 'content', 'custom_metadata', 'knowledge_base_folder', "created_by", "updated_by")  # 指定导入的字段
        skip_unchanged = True
        skip_empty = True
        report_skipped = True
        use_bulk = True

    def before_import(self, dataset, **kwargs):
        cleaned_data = []

        for row in dataset.dict:
            if not any(row.values()):  # 过滤空数据
                continue
            else:
                row["custom_metadata"] = json.dumps(row.get("custom_metadata", "").split(","))
                row["knowledge_base_folder"] = kwargs.get("knowledge_base_folder").id
                row["created_by"] = kwargs.get("created_by").id
                row["updated_by"] = kwargs.get("updated_by").id
                logging.log(logging.DEBUG, row)
                cleaned_data.append(row)

        dataset.dict = cleaned_data

    def after_init_instance(self, instance, new, row, **kwargs):
        instance.knowledge_base_folder = kwargs["knowledge_base_folder"]
        instance.created_by = kwargs["created_by"]
        instance.updated_by = kwargs["updated_by"]
