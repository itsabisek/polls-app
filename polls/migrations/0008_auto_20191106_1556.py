# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('polls', '0007_auto_20191106_1554'),
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=100)),
                ('username', models.CharField(max_length=100)),
                ('password', models.CharField(max_length=128)),
                ('uuid', models.CharField(max_length=128)),
            ],
        ),
        migrations.AlterField(
            model_name='answered',
            name='answered_on',
            field=models.DateTimeField(default=datetime.datetime(2019, 11, 6, 10, 26, 3, 517878, tzinfo=utc), verbose_name=b'answered date'),
        ),
        migrations.AlterField(
            model_name='question',
            name='asked_date',
            field=models.DateTimeField(default=datetime.datetime(2019, 11, 6, 10, 26, 3, 518586, tzinfo=utc), verbose_name=b'date asked'),
        ),
    ]
