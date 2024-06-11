from django.contrib import admin
from django.contrib import messages
from django.db.models import TextField
from django.forms import Media
from django.http import HttpRequest
from django.shortcuts import redirect
from django.urls import reverse
from django.utils.html import format_html
from unfold.admin import ModelAdmin
from unfold.contrib.forms.widgets import WysiwygWidget
from unfold.decorators import action
from apps.knowledge_mgmt.models import KnowledgeBaseFolder, FileKnowledge, ManualKnowledge, WebPageKnowledge
from apps.knowledge_mgmt.tasks.embed_task import general_embed


class FileKnowledgeInline(admin.TabularInline):
    model = FileKnowledge
    readonly_fields = ['title']


class WebPageKnowledgeInline(admin.TabularInline):
    model = WebPageKnowledge
    fieldsets = (
        ('', {
            'fields': ('title', 'url')
        }),
    )


class ManualKnowledgeInline(admin.StackedInline):
    model = ManualKnowledge
    fieldsets = (
        ('', {
            'fields': ('title', 'content')
        }),
    )
    formfield_overrides = {
        TextField: {
            "widget": WysiwygWidget,
        },
    }


@admin.register(KnowledgeBaseFolder)
class KnowledgeBaseFolderAdmin(ModelAdmin):
    list_display = ['name', 'description', 'embed_model_link',
                    'enable_text_search', 'enable_vector_search',
                    'train_status', 'train_progress']
    search_fields = ['name']
    list_display_links = ['name']
    ordering = ['id']
    filter_horizontal = []
    actions_row = ['train_embed']
    inlines = [FileKnowledgeInline, WebPageKnowledgeInline, ManualKnowledgeInline]
    readonly_fields = ['train_status']
    save_as = True

    fieldsets = (
        ('基本信息', {
            'fields': ('name', 'description')
        }),
        ('Embeding模型', {
            'fields': ('embed_model',)
        }),
        ('分块解析', {
            'fields': ('enable_general_parse', ('general_parse_chunk_size', 'general_parse_chunk_overlap'))
        }),

        ('文本检索', {
            'fields': ('enable_text_search', 'text_search_weight')
        }),

        ('向量检索', {
            'fields': ('enable_vector_search', 'vector_search_weight', 'rag_k', 'rag_num_candidates')
        }),
        ('结果重排', {
            'fields': ('enable_rerank', 'rerank_model', 'rerank_top_k')
        }),

    )

    @action(description='训练', url_path="train_embed_model")
    def train_embed(self, request: HttpRequest, object_id: int):
        general_embed.delay(object_id)
        messages.success(request, '开始训练')
        return redirect(reverse('admin:knowledge_mgmt_knowledgebasefolder_changelist'))

    def embed_model_link(self, obj):
        link = reverse("admin:model_provider_mgmt_embedprovider_change", args=[obj.embed_model.id])
        return format_html('<a href="{}">{}</a>', link, obj.embed_model)

    embed_model_link.short_description = '嵌入模型'
