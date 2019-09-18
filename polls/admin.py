from django.contrib import admin
from .models import Question, Choice


# Register your models here.
class ChoiceInline(admin.TabularInline):
    model = Choice
    extra = 1


class QuestionAdmin(admin.ModelAdmin):
    list_display = ('question_text', 'asked_date', 'was_published_recently')

    fieldsets = [
        (None, {'fields': ['question_text']}),
        ("Question Information", {"fields": ["asked_date", "description"],
                                  "classes": ['collapse']})
    ]

    inlines = [ChoiceInline]
    list_filter = ['asked_date']
    search_fields = ['question_text']
    # fields = ['asked_date', 'question_text', 'description']


admin.site.register(Question, QuestionAdmin)
