from django.contrib import admin
from django.db.models import TextField
from django.forms import JSONField
from django.urls import reverse
from django.utils.html import format_html
from django_ace import AceWidget
from import_export.admin import ImportExportModelAdmin
from unfold.contrib.forms.widgets import WysiwygWidget

from apps.core.admin.guarded_admin_base import GuardedAdminBase
from apps.knowledge_mgmt.models import ManualKnowledge
from apps.knowledge_mgmt.resources.manual_knowledge_resource import (
    ManualKnowledgeConfirmImportForm,
    ManualKnowledgeImportForm,
    ManualKnowledgeResource,
)


@admin.register(ManualKnowledge)
class ManualKnowledgeAdmin(GuardedAdminBase, ImportExportModelAdmin):
    def get_list_display(self, request):
        list_display = ["title", "knowledge_base_folder_link"]
        if request.user.is_superuser:
            list_display.append("owner_name")
        return list_display

    search_fields = ["title"]
    list_display_links = ["title"]
    list_filter = ["knowledge_base_folder"]
    ordering = ["id"]
    filter_horizontal = []
    fieldsets = (("", {"fields": ("knowledge_base_folder", "title", "content", "custom_metadata")}),
                 ("分块解析",
                  {"fields": ("enable_general_parse", ("general_parse_chunk_size", "general_parse_chunk_overlap"))}),
                 ("语义分块解析",
                  {"fields": ("enable_semantic_chunck_parse", "semantic_chunk_parse_embedding_model")}),
                 )
    formfield_overrides = {
        TextField: {
            "widget": WysiwygWidget,
        },
        JSONField: {"widget": AceWidget(mode="json", theme="chrome", width="700px")},
    }
    resource_classes = [ManualKnowledgeResource]
    import_form_class = ManualKnowledgeImportForm
    confirm_form_class = ManualKnowledgeConfirmImportForm

    import_error_display = "traceback"

    def knowledge_base_folder_link(self, obj):
        link = reverse("admin:knowledge_mgmt_knowledgebasefolder_change", args=[obj.knowledge_base_folder.id])
        return format_html('<a href="{}">{}</a>', link, obj.knowledge_base_folder)

    knowledge_base_folder_link.short_description = "知识库"

    def get_confirm_form_initial(self, request, import_form):
        initial = super().get_confirm_form_initial(request, import_form)

        if import_form:
            initial["knowledge_base_folder"] = import_form.cleaned_data["knowledge_base_folder"]
        return initial

    def get_import_data_kwargs(self, request, *args, **kwargs):
        """
        Prepare kwargs for import_data.
        """
        form = kwargs.get("form", None)
        if form and hasattr(form, "cleaned_data"):
            kwargs.update({"knowledge_base_folder": form.cleaned_data.get("knowledge_base_folder")})
            kwargs.update({"owner": request.user})
        return kwargs
