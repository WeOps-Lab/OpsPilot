from apps.contentpack_mgmt.models import (
    BotActions,
    ContentPack,
    Intent,
    RasaEntity,
    RasaForms,
    RasaResponse,
    RasaRules,
    RasaSlots,
    RasaStories,
)
from django.contrib import admin
from unfold.admin import ModelAdmin


class RasaStoriesInline(admin.TabularInline):
    model = RasaStories
    fields = ["name"]
    readonly_fields = ["name"]
    show_change_link = True
    extra = 0
    can_delete = False

    def has_add_permission(self, request, obj=None):
        return False


class BotActionsInline(admin.TabularInline):
    model = BotActions
    fields = ["name"]
    readonly_fields = ["name"]
    show_change_link = True
    extra = 0
    can_delete = False

    def has_add_permission(self, request, obj=None):
        return False


class RasaRulesInline(admin.TabularInline):
    model = RasaRules
    fields = ["name"]
    readonly_fields = ["name"]
    show_change_link = True
    extra = 0
    can_delete = False

    def has_add_permission(self, request, obj=None):
        return False


class IntentInline(admin.TabularInline):
    model = Intent

    fields = ["name"]
    readonly_fields = ["name"]
    show_change_link = True
    extra = 0
    can_delete = False

    def has_add_permission(self, request, obj=None):
        return False


class RasaFormsInline(admin.TabularInline):
    model = RasaForms

    fields = ["name"]
    readonly_fields = ["name"]
    show_change_link = True
    extra = 0
    can_delete = False

    def has_add_permission(self, request, obj=None):
        return False


class RasaSlotsInline(admin.TabularInline):
    model = RasaSlots

    fields = ["name"]
    readonly_fields = ["name"]
    show_change_link = True
    extra = 0
    can_delete = False

    def has_add_permission(self, request, obj=None):
        return False


class RasaEntityInline(admin.TabularInline):
    model = RasaEntity

    fields = ["name"]
    readonly_fields = ["name"]
    show_change_link = True
    extra = 0
    can_delete = False

    def has_add_permission(self, request, obj=None):
        return False


class RasaResponseInline(admin.TabularInline):
    model = RasaResponse

    fields = ["name"]
    readonly_fields = ["name"]
    show_change_link = True
    extra = 0
    can_delete = False

    def has_add_permission(self, request, obj=None):
        return False


@admin.register(ContentPack)
class ContentPackAdmin(ModelAdmin):
    list_display = ["name"]
    search_fields = ["name"]
    list_filter = ["name"]
    list_display_links = ["name"]
    ordering = ["id"]
    filter_horizontal = []
    inlines = [
        RasaStoriesInline,
        BotActionsInline,
        RasaRulesInline,
        IntentInline,
        RasaFormsInline,
        RasaSlotsInline,
        RasaEntityInline,
        RasaResponseInline,
    ]
