from django.contrib import admin

from apps.ops_pilot.models import Bot, Intent, IntentCorpus, Actions, Entities, SlotForm, Rules, Responses, \
    ResponseCorpus, Stories
from apps.ops_pilot.models.slots import Slots


@admin.register(Bot)
class BotAdmin(admin.ModelAdmin):
    list_display = (
        'name', 'description', 'is_active', 'session_expiration_time', 'carry_over_slots_to_new_session')
    list_display_links = ('name',)
    list_filter = ('is_active',)
    search_fields = ('name', 'description')
    list_editable = ('is_active', 'session_expiration_time', 'carry_over_slots_to_new_session')
    list_per_page = 10
    ordering = ('id',)
    filter_horizontal = ('rules', 'stories')


class IntentCorpusInline(admin.TabularInline):
    model = IntentCorpus
    extra = 0
    can_delete = True
    fields = ('corpus',)
    show_change_link = True


@admin.register(Intent)
class IntentAdmin(admin.ModelAdmin):
    list_display = ('name', 'description')
    list_display_links = ('name',)
    search_fields = ('name', 'description')
    list_per_page = 10
    ordering = ('id',)
    inlines = [IntentCorpusInline]


@admin.register(IntentCorpus)
class IntentCorpusAdmin(admin.ModelAdmin):
    list_display = ('intent', 'corpus')
    list_display_links = ('corpus',)
    search_fields = ('corpus',)
    list_per_page = 10
    ordering = ('id',)
    autocomplete_fields = ('intent',)


@admin.register(Actions)
class ActionsAdmin(admin.ModelAdmin):
    list_display = ('name', 'action_func', 'description')
    list_display_links = ('name',)
    search_fields = ('name', 'action_func', 'description')
    list_per_page = 10
    ordering = ('id',)


@admin.register(Entities)
class EntitiesAdmin(admin.ModelAdmin):
    list_display = ('name', 'description')
    list_display_links = ('name',)
    search_fields = ('name', 'description')
    list_per_page = 10
    ordering = ('id',)


@admin.register(Slots)
class SlotsAdmin(admin.ModelAdmin):
    list_display = ('name', 'description', 'slot_type', 'influence_conversation', 'description')
    list_display_links = ('name',)
    search_fields = ('name', 'description', 'slot_type')
    list_per_page = 10
    ordering = ('id',)


@admin.register(SlotForm)
class SlotFormAdmin(admin.ModelAdmin):
    list_display = ('name', 'description')
    list_display_links = ('name',)
    search_fields = ('name',)
    list_per_page = 10
    ordering = ('id',)


@admin.register(Rules)
class RulesAdmin(admin.ModelAdmin):
    list_display = ('name', 'description')
    list_display_links = ('name',)
    search_fields = ('name', 'description')
    list_per_page = 10
    ordering = ('id',)


class ResponseCorpusInline(admin.TabularInline):
    model = ResponseCorpus
    extra = 0
    can_delete = True
    fields = ('text', 'channel')
    show_change_link = True


@admin.register(Responses)
class ResponsesAdmin(admin.ModelAdmin):
    list_display = ('name',)
    list_display_links = ('name',)
    search_fields = ('name',)
    list_per_page = 10
    ordering = ('id',)
    inlines = [ResponseCorpusInline]


@admin.register(ResponseCorpus)
class ResponseCorpusAdmin(admin.ModelAdmin):
    list_display = ('text', 'channel')
    list_display_links = ('text',)
    search_fields = ('text', 'channel')
    list_per_page = 10
    ordering = ('id',)


@admin.register(Stories)
class StoriesAdmin(admin.ModelAdmin):
    list_display = ('name', 'description')
    list_display_links = ('name',)
    search_fields = ('name', 'description')
    list_per_page = 10
    ordering = ('id',)
