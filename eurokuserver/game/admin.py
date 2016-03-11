from django.contrib import admin
from .models import Question, Game
# Register your models here.


class QuestionAdmin(admin.ModelAdmin):
    date_hierarchy = "added"
    list_display = ('title', 'correct_answer', 'public', 'added')
    list_filter = ('lang', 'provider')
    actions = ['unpublish', 'publish']

    def unpublish(self, request, queryset):
        updated = queryset.update(public=False)
        self.message_user(request, '{} galdera aldatuta'.format(updated))
    unpublish.short_description = u'Unpublish'

    def publish(self, request, queryset):
        updated = queryset.update(public=True)
        self.message_user(request, '{} galdera aldatuta'.format(updated))
    publish.short_description = u'Publish'

admin.site.register(Question, QuestionAdmin)
admin.site.register(Game)

