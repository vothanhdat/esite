# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2017-07-13 07:56
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('econ', '0014_auto_20170713_0716'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='productoptionspecdetail',
            unique_together=set([]),
        ),
        migrations.RemoveField(
            model_name='productoptionspecdetail',
            name='prod_option',
        ),
        migrations.RemoveField(
            model_name='productoptionspecdetail',
            name='spec',
        ),
        migrations.RemoveField(
            model_name='productoptionspecdetail',
            name='specof',
        ),
        migrations.AddField(
            model_name='productspecdetail',
            name='prod_option',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='econ.ProductOption'),
        ),
        migrations.AlterUniqueTogether(
            name='productspecdetail',
            unique_together=set([('specof', 'prod', 'prod_option')]),
        ),
        migrations.DeleteModel(
            name='ProductOptionSpecDetail',
        ),
    ]
