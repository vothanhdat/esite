# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2017-07-13 11:20
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('econ', '0018_auto_20170713_1118'),
    ]

    operations = [
        migrations.AlterField(
            model_name='productoption',
            name='prod',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='econ.Product'),
        ),
    ]
