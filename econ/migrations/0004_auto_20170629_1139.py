# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2017-06-29 11:39
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('econ', '0003_auto_20170629_1136'),
    ]

    operations = [
        migrations.AlterField(
            model_name='productpromotion',
            name='apply_to',
            field=models.ManyToManyField(blank=True, null=True, to='econ.Product'),
        ),
    ]
