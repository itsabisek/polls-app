from django.db import models
from django.utils import timezone
import datetime


# Create your models here.
class Question(models.Model):
    question_text = models.CharField(max_length=200)
    description = models.CharField(max_length=1000)
    asked_date = models.DateTimeField('date asked')

    def was_published_recently(self):
        return self.asked_date > timezone.now() - datetime.timedelta(days=1)

    was_published_recently.admin_order_field = 'asked_date'
    was_published_recently.boolean = True
    was_published_recently.short_description = 'Published Recently?'

    def __unicode__(self):
        return self.question_text


class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=128)
    votes = models.IntegerField(default=0)

    def __unicode__(self):
        return self.choice_text
