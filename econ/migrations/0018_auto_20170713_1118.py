# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2017-07-13 11:18
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('econ', '0017_auto_20170713_1056'),
    ]

    operations = [
        migrations.AlterField(
            model_name='productspecdetail',
            name='prod',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='econ.Product'),
        ),
        migrations.AlterField(
            model_name='productspecdetail',
            name='prod_option',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='econ.ProductOption'),
        ),
    ]
