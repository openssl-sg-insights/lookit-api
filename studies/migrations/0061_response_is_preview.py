# -*- coding: utf-8 -*-
# Generated by Django 1.11.23 on 2020-02-19 16:55
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [("studies", "0060_auto_20200219_1036")]

    operations = [
        migrations.AddField(
            model_name="response",
            name="is_preview",
            field=models.BooleanField(default=False),
        )
    ]
