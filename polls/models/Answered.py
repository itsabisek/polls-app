from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
import datetime


class Answered(models.Model):
    """

        Answered model: Creates table named Answered that stores user id and question id
        that the user corresponding to the user id answered

    """
    user_id = models.IntegerField(null=False)
    question_id = models.IntegerField(null=False)
    answered_on = models.DateTimeField(
        'answered date', default=timezone.now, null=False)

    def __unicode__(self):
        return "User : %s Question : %s" % (str(self.user_id), str(self.question_id))
