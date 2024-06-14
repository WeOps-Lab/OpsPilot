import json

from apps.knowledge_mgmt.models import KnowledgeBaseFolder, ManualKnowledge
from django import forms
from import_export import resources
from import_export.forms import ConfirmImportForm, ImportForm
from loguru import logger


class ManualKnowledgeImportForm(ImportForm):
    knowledge_base_folder = forms.ModelChoiceField(
        queryset=KnowledgeBaseFolder.objects.all(), required=True, label="请选择需要导入的知识库"
    )
    field_order = ["knowledge_base_folder", "import_file", "format"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # 设置 resource 字段为隐藏字段
        self.fields["resource"].widget = forms.HiddenInput()
        self.fields["resource"].label = ""  # 设置为一个空字符串


class ManualKnowledgeConfirmImportForm(ConfirmImportForm):
    knowledge_base_folder = forms.ModelChoiceField(
        queryset=KnowledgeBaseFolder.objects.all(), required=True, label="请选择需要导入的知识库"
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # 设置 resource 字段为隐藏字段
        self.fields["knowledge_base_folder"].widget = forms.HiddenInput()
        self.fields["knowledge_base_folder"].label = ""  # 设置为一个空字符串


class ManualKnowledgeResource(resources.ModelResource):
    class Meta:
        model = ManualKnowledge
        import_id_fields = ("title",)
        fields = (
            "title",
            "content",
            "custom_metadata",
            "knowledge_base_folder",
            "owner",
        )  # 指定导入的字段
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
                row["owner"] = kwargs.get("owner").id
                logger.debug(row)
                cleaned_data.append(row)

        dataset.dict = cleaned_data

    def after_init_instance(self, instance, new, row, **kwargs):
        super().after_init_instance(instance, new, row, **kwargs)
        instance.knowledge_base_folder = kwargs["knowledge_base_folder"]
        instance.owner = kwargs["owner"]
