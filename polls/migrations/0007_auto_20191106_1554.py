# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('polls', '0006_auto_20191106_1552'),
    ]

    operations = [
        migrations.AlterField(
            model_name='answered',
            name='answered_on',
            field=models.DateTimeField(default=datetime.datetime(2019, 11, 6, 10, 24, 14, 530969, tzinfo=utc), verbose_name=b'answered date'),
        ),
        migrations.AlterField(
            model_name='question',
            name='asked_date',
            field=models.DateTimeField(default=datetime.datetime(2019, 11, 6, 10, 24, 14, 531591, tzinfo=utc), verbose_name=b'date asked'),
        ),
    ]
