# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2017-07-13 10:54
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('econ', '0015_auto_20170713_0756'),
    ]

    operations = [
        migrations.AlterField(
            model_name='productspecdetail',
            name='prod',
            field=models.ForeignKey(editable=False, on_delete=django.db.models.deletion.CASCADE, to='econ.Product'),
        ),
        migrations.AlterField(
            model_name='productspecdetail',
            name='prod_option',
            field=models.ForeignKey(blank=True, editable=False, null=True, on_delete=django.db.models.deletion.CASCADE, to='econ.ProductOption'),
        ),
    ]
