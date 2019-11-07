import datetime
from django.utils import timezone
from django.db import models
from .Question import Question


class Choice(models.Model):
    """
        Choice model: Creates table named Choice to store all choices with attributes
        choice text and number of votes the choice received .Backrefs to the Question 
        the choice belongs to

    """
    question = models.ForeignKey(
        Question, on_delete=models.CASCADE, null=False)
    choice_text = models.CharField(max_length=128, null=False)
    votes = models.IntegerField(default=0, null=False)

    def __unicode__(self):
        return self.choice_text
