# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('polls', '0004_answered_answered_on'),
    ]

    operations = [
        migrations.AlterField(
            model_name='answered',
            name='answered_on',
            field=models.DateTimeField(default=datetime.datetime(2019, 10, 23, 11, 7, 10, 520899, tzinfo=utc), verbose_name=b'answered date'),
        ),
        migrations.AlterField(
            model_name='question',
            name='asked_date',
            field=models.DateTimeField(default=datetime.datetime(2019, 10, 23, 11, 7, 10, 519010, tzinfo=utc), verbose_name=b'date asked'),
        ),
    ]
