# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2018-02-18 01:58
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('clients', '0002_socialnetwork'),
    ]

    operations = [
        migrations.AddField(
            model_name='socialnetwork',
            name='facebook',
            field=models.URLField(blank=True),
        ),
        migrations.AddField(
            model_name='socialnetwork',
            name='github',
            field=models.URLField(blank=True),
        ),
        migrations.AddField(
            model_name='socialnetwork',
            name='twitter',
            field=models.URLField(blank=True),
        ),
    ]
