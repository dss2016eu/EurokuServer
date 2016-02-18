from django.contrib import admin
from .models import Question, Game
# Register your models here.

class QuestionAdmin(admin.ModelAdmin):
    date_hierarchy = "added"
    list_display = ('title', 'correct_answer', 'public', 'added')
    list_filter = ('lang', 'provider')
admin.site.register(Question, QuestionAdmin)
admin.site.register(Game)

