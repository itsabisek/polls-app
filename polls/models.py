from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
import datetime


# Create your models here.
class Question(models.Model):
    # user = models.ForeignKey(User, on_delete=models.CASCADE)
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


class Answered(models.Model):
    user_id = models.IntegerField()
    question_id = models.IntegerField()

    def __unicode__(self):
        return "User : %s Question : %s" % (str(self.user_id), str(self.question_id))
