from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
import datetime


# Question model: Creates table named question with attributes question
# and date the question was asked
# Backrefs to the user who asked this question
class Question(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=0)
    question_text = models.CharField(max_length=200)
    asked_date = models.DateTimeField('date asked', default=timezone.now())

    # Returns True if poll was created with last 1 day; False otherwise
    def was_published_recently(self):
        return self.asked_date > timezone.now() - datetime.timedelta(days=1)

    was_published_recently.admin_order_field = 'asked_date'
    was_published_recently.boolean = True
    was_published_recently.short_description = 'Published Recently?'

    def __unicode__(self):
        return self.question_text


# Choice model: Creates table named Choice to store all choices with attributes
# choice text and number of votes the choice received
# Backrefs to the Question the choice belongs to
class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=128)
    votes = models.IntegerField(default=0)

    def __unicode__(self):
        return self.choice_text


# Answered model: Creates table named Answered that stores user id and question id
# that the user corresponding to the user id answered
class Answered(models.Model):
    user_id = models.IntegerField()
    question_id = models.IntegerField()
    answered_on = models.DateTimeField('answered date', default=timezone.now())

    def __unicode__(self):
        return "User : %s Question : %s" % (str(self.user_id), str(self.question_id))
