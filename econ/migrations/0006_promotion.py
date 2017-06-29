# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2017-06-29 09:25
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('econ', '0005_auto_20170629_0912'),
    ]

    operations = [
        migrations.CreateModel(
            name='Promotion',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('promotion_name', models.CharField(max_length=100)),
                ('promotion_type', models.CharField(choices=[(b'M', b'Minus'), (b'P', b'Percentage'), (b'O', b'Offer')], default=b'P', max_length=1)),
                ('promotion_value', models.FloatField()),
            ],
        ),
    ]