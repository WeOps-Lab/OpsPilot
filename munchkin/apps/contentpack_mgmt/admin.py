from django.contrib import admin, messages
from django.utils.html import format_html
from unfold.decorators import action
from django.http import HttpRequest
from django.shortcuts import redirect
from django.urls import reverse
from django_ace import AceWidget
from django_yaml_field import YAMLField
from unfold.admin import ModelAdmin

from apps.contentpack_mgmt.models import BotActions, BotActionRule, RasaEntity, Intent, IntentCorpus, RasaRules, \
    RasaStories, RasaResponse, RasaResponseCorpus, RasaForms, RasaSlots, ContentPack, RasaModel

from apps.contentpack_mgmt.tasks.contentpack_task import build_rasa_train_data

from apps.core.utils.kubernetes_client import KubernetesClient


@admin.register(BotActions)
class BotActionsAdmin(ModelAdmin):
    list_display = ['content_pack_link', 'name']
    search_fields = ['name']
    list_filter = ['content_pack', 'name']
    list_display_links = ['name']
    ordering = ['id']
    filter_horizontal = []

    def content_pack_link(self, obj):
        link = reverse("admin:contentpack_mgmt_contentpack_change", args=[obj.content_pack.id])
        return format_html('<a href="{}">{}</a>', link, obj.content_pack)

    content_pack_link.short_description = '扩展包'


class BotActionsInline(admin.TabularInline):
    model = BotActions
    fields = ['name']
    readonly_fields = ['name']
    show_change_link = True
    extra = 0
    can_delete = False

    def has_add_permission(self, request, obj=None):
        return False


@admin.register(BotActionRule)
class BotActionRuleAdmin(ModelAdmin):
    list_display = ['name', 'bot_action_link', 'channel_link']
    search_fields = ['name']
    list_filter = ['name']
    list_display_links = ['name']
    ordering = ['id']
    filter_horizontal = ['rule_user_groups', 'rule_user']

    def bot_action_link(self, obj):
        link = reverse("admin:contentpack_mgmt_botactions_change", args=[obj.bot_action.id])
        return format_html('<a href="{}">{}</a>', link, obj.bot_action)

    bot_action_link.short_description = '动作'

    def channel_link(self, obj):
        if obj.channel is None:
            return '-'
        else:
            link = reverse("admin:channel_mgmt_channel_change", args=[obj.channel.id])
            return format_html('<a href="{}">{}</a>', link, obj.channel)

    channel_link.short_description = '通道'


@admin.register(RasaEntity)
class RasaEntityAdmin(ModelAdmin):
    list_display = ['content_pack_link', 'name']
    search_fields = ['name']
    list_filter = ['content_pack', 'name']
    list_display_links = ['name']
    ordering = ['id']
    filter_horizontal = []

    def content_pack_link(self, obj):
        link = reverse("admin:contentpack_mgmt_contentpack_change", args=[obj.content_pack.id])
        return format_html('<a href="{}">{}</a>', link, obj.content_pack)

    content_pack_link.short_description = '扩展包'


class RasaEntityInline(admin.TabularInline):
    model = RasaEntity

    fields = ['name']
    readonly_fields = ['name']
    show_change_link = True
    extra = 0
    can_delete = False

    def has_add_permission(self, request, obj=None):
        return False


class IntentCorpusInline(admin.TabularInline):
    model = IntentCorpus
    show_change_link = True
    extra = 0


@admin.register(Intent)
class IntentAdmin(ModelAdmin):
    list_display = ['content_pack_link', 'name']
    search_fields = ['name']
    list_filter = ['content_pack', 'name']
    list_display_links = ['name']
    ordering = ['id']
    filter_horizontal = []
    inlines = [
        IntentCorpusInline
    ]

    def content_pack_link(self, obj):
        link = reverse("admin:contentpack_mgmt_contentpack_change", args=[obj.content_pack.id])
        return format_html('<a href="{}">{}</a>', link, obj.content_pack)

    content_pack_link.short_description = '扩展包'


class IntentInline(admin.TabularInline):
    model = Intent

    fields = ['name']
    readonly_fields = ['name']
    show_change_link = True
    extra = 0
    can_delete = False

    def has_add_permission(self, request, obj=None):
        return False


@admin.register(IntentCorpus)
class IntentCorpusAdmin(ModelAdmin):
    list_display = ['content_pack_link', 'intent_link', 'corpus']
    search_fields = ['corpus']
    list_filter = ['intent']
    list_display_links = ['corpus']
    ordering = ['id']
    filter_horizontal = []

    def content_pack_link(self, obj):
        link = reverse("admin:contentpack_mgmt_contentpack_change", args=[obj.intent.content_pack.id])
        return format_html('<a href="{}">{}</a>', link, obj.intent.content_pack)

    content_pack_link.short_description = '扩展包'

    def intent_link(self, obj):
        link = reverse("admin:contentpack_mgmt_intent_change", args=[obj.intent.id])
        return format_html('<a href="{}">{}</a>', link, obj.intent)

    intent_link.short_description = '意图'


@admin.register(RasaRules)
class RasaRulesAdmin(ModelAdmin):
    list_display = ['content_pack_link', 'name']
    search_fields = ['name']
    list_filter = ['content_pack', 'name']
    list_display_links = ['name']
    ordering = ['id']
    filter_horizontal = []
    formfield_overrides = {YAMLField: {
        "widget": AceWidget(mode="yaml", theme='chrome', width='700px')}
    }

    def content_pack_link(self, obj):
        link = reverse("admin:contentpack_mgmt_contentpack_change", args=[obj.content_pack.id])
        return format_html('<a href="{}">{}</a>', link, obj.content_pack)

    content_pack_link.short_description = '扩展包'


class RasaRulesInline(admin.TabularInline):
    model = RasaRules
    fields = ['name']
    readonly_fields = ['name']
    show_change_link = True
    extra = 0
    can_delete = False

    def has_add_permission(self, request, obj=None):
        return False


@admin.register(RasaStories)
class RasaStoriesAdmin(ModelAdmin):
    list_display = ['content_pack_link', 'name']
    search_fields = ['name']
    list_filter = ['content_pack', 'name']
    list_display_links = ['name']
    ordering = ['id']
    filter_horizontal = []
    formfield_overrides = {YAMLField: {
        "widget": AceWidget(mode="yaml", theme='chrome', width='700px')}
    }

    def content_pack_link(self, obj):
        link = reverse("admin:contentpack_mgmt_contentpack_change", args=[obj.content_pack.id])
        return format_html('<a href="{}">{}</a>', link, obj.content_pack)

    content_pack_link.short_description = '扩展包'


class RasaStoriesInline(admin.TabularInline):
    model = RasaStories
    fields = ['name']
    readonly_fields = ['name']
    show_change_link = True
    extra = 0
    can_delete = False

    def has_add_permission(self, request, obj=None):
        return False


class RasaResponseCorpusInline(admin.TabularInline):
    model = RasaResponseCorpus
    show_change_link = True
    extra = 0


@admin.register(RasaResponse)
class RasaResponseAdmin(ModelAdmin):
    list_display = ['content_pack_link', 'name']
    search_fields = ['name']
    list_filter = ['content_pack', 'name']
    list_display_links = ['name']
    ordering = ['id']
    filter_horizontal = []
    inlines = [RasaResponseCorpusInline]

    def content_pack_link(self, obj):
        link = reverse("admin:contentpack_mgmt_contentpack_change", args=[obj.content_pack.id])
        return format_html('<a href="{}">{}</a>', link, obj.content_pack)

    content_pack_link.short_description = '扩展包'


class RasaResponseInline(admin.TabularInline):
    model = RasaResponse

    fields = ['name']
    readonly_fields = ['name']
    show_change_link = True
    extra = 0
    can_delete = False

    def has_add_permission(self, request, obj=None):
        return False


@admin.register(RasaResponseCorpus)
class RasaResponseCorpusAdmin(ModelAdmin):
    list_display = ['response', 'corpus']
    search_fields = ['corpus']
    list_filter = ['response']
    list_display_links = ['corpus']
    ordering = ['id']
    filter_horizontal = []


@admin.register(RasaForms)
class RasaFormsAdmin(ModelAdmin):
    list_display = ['content_pack_link', 'name']
    search_fields = ['name']
    list_filter = ['content_pack', 'name']
    list_display_links = ['name']
    ordering = ['id']
    filter_horizontal = []
    formfield_overrides = {YAMLField: {
        "widget": AceWidget(mode="yaml", theme='chrome', width='700px')}
    }

    def content_pack_link(self, obj):
        link = reverse("admin:contentpack_mgmt_contentpack_change", args=[obj.content_pack.id])
        return format_html('<a href="{}">{}</a>', link, obj.content_pack)

    content_pack_link.short_description = '扩展包'


class RasaFormsInline(admin.TabularInline):
    model = RasaForms

    fields = ['name']
    readonly_fields = ['name']
    show_change_link = True
    extra = 0
    can_delete = False

    def has_add_permission(self, request, obj=None):
        return False


@admin.register(RasaSlots)
class RasaSlotsAdmin(ModelAdmin):
    list_display = ['content_pack_link', 'name']
    search_fields = ['name']
    list_filter = ['content_pack', 'name']
    list_display_links = ['name']
    ordering = ['id']
    filter_horizontal = []
    formfield_overrides = {YAMLField: {
        "widget": AceWidget(mode="yaml", theme='chrome', width='700px')}
    }

    def content_pack_link(self, obj):
        link = reverse("admin:contentpack_mgmt_contentpack_change", args=[obj.content_pack.id])
        return format_html('<a href="{}">{}</a>', link, obj.content_pack)

    content_pack_link.short_description = '扩展包'


class RasaSlotsInline(admin.TabularInline):
    model = RasaSlots

    fields = ['name']
    readonly_fields = ['name']
    show_change_link = True
    extra = 0
    can_delete = False

    def has_add_permission(self, request, obj=None):
        return False


@admin.register(ContentPack)
class ContentPackAdmin(ModelAdmin):
    list_display = ['name']
    search_fields = ['name']
    list_filter = ['name']
    list_display_links = ['name']
    ordering = ['id']
    filter_horizontal = []
    inlines = [
        RasaStoriesInline,
        BotActionsInline,
        RasaRulesInline,
        IntentInline,
        RasaFormsInline,
        RasaSlotsInline,
        RasaEntityInline,
        RasaResponseInline
    ]


@admin.register(RasaModel)
class RasaModelAdmin(ModelAdmin):
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

    @action(description='训练', url_path="train_pilot")
    def train_pilot(self, request: HttpRequest, object_id: int):
        client = KubernetesClient('argo')

        workflow_id = client.train_pilot(object_id)
        model = RasaModel.objects.get(id=object_id)
        model.workflow_id = workflow_id
        model.save()

        messages.success(request, '开始训练')
        return redirect(reverse('admin:contentpack_mgmt_rasamodel_changelist'))
