"""Administrative resources related to resources."""

from django.contrib import admin

from .models import Day, Topic, Resource, make_published, make_private, Suggestion
from .forms import ResourceForm, TopicInlineForm


class TopicInline(admin.StackedInline):
    """Inlined topic list appearing on day form."""

    fields = ['title', 'description', 'status', 'position']
    sortable_field_name = 'position'
    model = Topic
    extra = 0
    ordering = ['position']
    form = TopicInlineForm


class DayAdmin(admin.ModelAdmin):
    """Day administrative pages."""

    prepopulated_fields = {'slug': ['title']}
    fieldsets = (
        (None, {
            'fields': (
                       'title',
                       'description',
                       'status',
            )}),
        ('Advanced', {
            'fields': ('id',
                       'slug',
                       'created',
                       'modified',
                       'status_changed',
            ),
            'classes': ('grp-collapse', 'grp-closed')}))
    readonly_fields = ['id', 'created', 'modified', 'status_changed']
    list_display = ('title', 'slug', 'description', 'is_active')
    search_fields = ['title', 'description']
    list_filter = ['status']
    list_display_links = ['title', 'slug']
    actions = [make_published, make_private]
    inlines = [TopicInline]

    class Media:
        """Additional CSS/JS to send out with this admin interface."""
        css = {"all": ["css/admin_extra.css"]}


class TopicAdmin(admin.ModelAdmin):
    """Topic administrative pages."""

    prepopulated_fields = {'slug': ['title']}
    fieldsets = (
        (None, {
            'fields': (
                       'title',
                       'description',
                       'day',
                       'status',
            )}),
        ('Advanced', {
            'fields': ('id',
                       'slug',
                       'created',
                       'modified',
                       'status_changed',
            ),
            'classes': ('grp-collapse', 'grp-closed')}))
    readonly_fields = ['id', 'created', 'modified', 'status_changed']
    list_display = ('day', 'title', 'slug', 'description', 'is_active')
    search_fields = ['day__title', 'title', 'description']
    list_filter = ['day', 'status']
    list_display_links = ['title', 'slug']
    actions = [make_published, make_private]
    ordering = ['day', 'position']


class ResourceAdmin(admin.ModelAdmin):
    """Resource administrative pages."""

    prepopulated_fields = {'slug': ['title']}
    fieldsets = (
        (None, {
            'fields': (
                'title',
                'description',
                'topic',
                'link',
                'file',
                'key',
                'required',
                'status',
            )}),
        ('Advanced', {
            'fields': ('id',
                       'slug',
                       'file_size',
                       'file_mimetype',
                       'created',
                       'modified',
                       'status_changed',
                       'is_more',
            ),
            'classes': ('grp-collapse', 'grp-closed')}))
    readonly_fields = ['id', 'created', 'modified', 'status_changed', 'file_size', 'file_mimetype']
    list_display = ('topic', 'title', 'slug', 'description', 'key', 'required', 'is_active')
    search_fields = ['title', 'description', 'topic__title']
    list_filter = ['topic', 'status']
    list_display_links = ['title', 'slug']
    actions = [make_published, make_private]
    ordering = ['topic', 'title']
    form = ResourceForm


class SuggestionAdmin(admin.ModelAdmin):
    """Suggestion administrative pages."""

    readonly_fields = ['created']
    list_display = ('title', 'description', 'created', 'name')
    search_fields = ('title', 'description', 'name', 'email')


admin.site.register(Day, DayAdmin)
admin.site.register(Topic, TopicAdmin)
admin.site.register(Resource, ResourceAdmin)
admin.site.register(Suggestion, SuggestionAdmin)