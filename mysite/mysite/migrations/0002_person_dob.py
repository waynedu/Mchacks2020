# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2017-11-26 06:11
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mysite', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='person',
            name='dob',
            field=models.CharField(default=0, max_length=50),
            preserve_default=False,
        ),
    ]
