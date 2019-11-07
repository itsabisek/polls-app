from django.db import models
import uuid


class User(models.Model):
    name = models.CharField(max_length=100, null=False)
    username = models.CharField(max_length=100, null=False)
    password = models.CharField(max_length=128, null=False)
    uuid = models.CharField(max_length=128, null=False)

    def is_authenticated(self):
        return True

    def __str__(self):
        return "%s : %s" % (self.username, self.uuid)
