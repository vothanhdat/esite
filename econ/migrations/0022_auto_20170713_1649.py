# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2017-07-13 16:49
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('econ', '0021_auto_20170713_1305'),
    ]

    operations = [
        migrations.AlterField(
            model_name='productspecdetail',
            name='prod',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='econ.Product'),
        ),
    ]
