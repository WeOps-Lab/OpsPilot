from apps.model_provider_mgmt.models import RerankProvider
from django.contrib import admin
from django.db.models import JSONField
from django_ace import AceWidget
from unfold.admin import ModelAdmin

from apps.model_provider_mgmt.models.ocr_provider import OCRProvider


@admin.register(OCRProvider)
class OCRProviderAdmin(ModelAdmin):
    list_display = ["name", "enabled"]
    search_fields = ["name"]
    list_filter = ["name"]
    list_display_links = ["name"]
    ordering = ["id"]
    filter_horizontal = []
    fieldsets = ((None, {"fields": ("name", "ocr_config", "enabled")}),)
    formfield_overrides = {JSONField: {"widget": AceWidget(mode="json", theme="chrome", width="700px")}}

    def has_module_permission(self, request):
        return request.user.is_superuser
