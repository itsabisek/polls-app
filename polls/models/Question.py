from django.db import models
from django.utils import timezone
from .User import User
import datetime


class Question(models.Model):
    """
        Question model: Creates table named question with attributes question 
        and date the question was asked. Backrefs to the user who asked this question

    """

    user = models.ForeignKey(
        User, on_delete=models.CASCADE, default=0, null=False)
    question_text = models.CharField(max_length=200, null=False)
    asked_date = models.DateTimeField(
        'date asked', default=timezone.now, null=False)

    # Returns True if poll was created with last 1 day; False otherwise
    def was_published_recently(self):
        return self.asked_date > timezone.now() - datetime.timedelta(days=1)

    was_published_recently.admin_order_field = 'asked_date'
    was_published_recently.boolean = True
    was_published_recently.short_description = 'Published Recently?'

    def __unicode__(self):
        return self.question_text
