# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('polls', '0003_answered'),
    ]

    operations = [
        migrations.AddField(
            model_name='answered',
            name='answered_on',
            field=models.DateTimeField(default=datetime.datetime(2019, 10, 18, 12, 52, 32, 13610, tzinfo=utc), verbose_name=b'answered date'),
            preserve_default=False,
        ),
    ]
