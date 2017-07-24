# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2017-07-24 08:36
from __future__ import unicode_literals

from django.db import migrations
import tagging.fields


class Migration(migrations.Migration):

    dependencies = [
        ('econ', '0002_auto_20170721_1719'),
    ]

    operations = [
        migrations.AlterField(
            model_name='taggedinfo',
            name='tags',
            field=tagging.fields.TagField(blank=True, default=None, max_length=255),
            preserve_default=False,
        ),
    ]
