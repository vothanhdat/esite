# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2017-07-19 10:13
from __future__ import unicode_literals

import ckeditor.fields
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('econ', '0006_remove_product_product_info'),
    ]

    operations = [
        migrations.AlterField(
            model_name='productinfo',
            name='info',
            field=ckeditor.fields.RichTextField(blank=True, null=True),
        ),
    ]
