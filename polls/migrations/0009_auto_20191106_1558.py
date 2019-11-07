# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.utils.timezone
import datetime
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('polls', '0008_auto_20191106_1556'),
    ]

    operations = [
        migrations.AlterField(
            model_name='answered',
            name='answered_on',
            field=models.DateTimeField(
                default=django.utils.timezone.now, verbose_name=b'answered date'),
        ),
        migrations.AlterField(
            model_name='question',
            name='asked_date',
            field=models.DateTimeField(
                default=django.utils.timezone.now, verbose_name=b'date asked'),
        ),
    ]
