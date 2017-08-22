# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2017-08-17 16:18
from __future__ import unicode_literals

import ckeditor.fields
from decimal import Decimal
from django.conf import settings
import django.contrib.auth.models
from django.db import migrations, models
import django.db.models.deletion
import djmoney.models.fields
import mptt.fields
import tagging.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0008_alter_user_username_max_length'),
        ('contenttypes', '0002_remove_content_type_name'),
        ('econ', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Agency',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('agency_name', models.CharField(blank=True, max_length=100, null=True)),
                ('agency_id', models.CharField(blank=True, max_length=20, null=True)),
                ('agency_logo', models.ImageField(blank=True, null=True, upload_to='media/%Y/%m/%d/%H/%M/%S/')),
            ],
        ),
        migrations.CreateModel(
            name='AgencyMember',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('agency', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='econ.Agency')),
            ],
        ),
        migrations.CreateModel(
            name='AgencyPromotion',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('promotion_name', models.CharField(max_length=100)),
                ('promotion_type', models.CharField(choices=[('M', 'Minus'), ('P', 'Percentage'), ('O', 'Offer')], default='P', max_length=1)),
                ('promotion_value', models.FloatField()),
                ('promotion_start', models.DateTimeField(null=True)),
                ('promotion_end', models.DateTimeField(null=True)),
                ('apply_to', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='econ.Agency')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='BaseUser',
            fields=[
                ('user_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to=settings.AUTH_USER_MODEL)),
                ('baseuser_bio', models.TextField(blank=True, max_length=500)),
                ('baseuser_address', models.TextField(blank=True, max_length=500)),
                ('baseuser_birthday', models.DateField(blank=True, null=True)),
                ('baseuser_gender', models.CharField(choices=[('U', 'Unknow'), ('M', 'Male'), ('F', 'Female')], default='U', max_length=1)),
                ('baseuser_avatar', models.ImageField(blank=True, null=True, upload_to='media/%Y/%m/%d/%H/%M/%S/')),
            ],
            options={
                'abstract': False,
                'verbose_name': 'user',
                'verbose_name_plural': 'users',
            },
            bases=('auth.user',),
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.CreateModel(
            name='Brand',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('brand_name', models.CharField(max_length=100)),
                ('brand_sym', models.CharField(max_length=20)),
                ('brand_logo', models.ImageField(blank=True, null=True, upload_to='media/%Y/%m/%d/%H/%M/%S/')),
                ('tags', tagging.fields.TagField(blank=True, max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='Cagetory',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cagetory_name', models.CharField(max_length=50)),
                ('tags', tagging.fields.TagField(blank=True, max_length=255)),
                ('optiontype', models.IntegerField(choices=[(1, 'Inherit'), (2, 'Option by specify'), (3, 'Option by generic')], default=1)),
                ('lft', models.PositiveIntegerField(db_index=True, editable=False)),
                ('rght', models.PositiveIntegerField(db_index=True, editable=False)),
                ('tree_id', models.PositiveIntegerField(db_index=True, editable=False)),
                ('level', models.PositiveIntegerField(db_index=True, editable=False)),
                ('parent', mptt.fields.TreeForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='children', to='econ.Cagetory')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('product_name', models.CharField(max_length=100)),
                ('product_price_currency', djmoney.models.fields.CurrencyField(choices=[('EUR', 'Euro'), ('USD', 'US Dollar'), ('VND', 'Vietnam Dong')], default='USD', editable=False, max_length=3)),
                ('product_price', djmoney.models.fields.MoneyField(decimal_places=2, default=Decimal('0.0'), default_currency='USD', max_digits=10)),
                ('product_quatity', models.IntegerField(default=0, verbose_name='numbers')),
                ('tags', tagging.fields.TagField(blank=True, max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='ProductImage',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(blank=True, null=True, upload_to='media/%Y/%m/%d/%H/%M/%S/')),
                ('image_link', models.CharField(blank=True, max_length=300, null=True)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='ProductOption',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('product_price_currency', djmoney.models.fields.CurrencyField(choices=[('EUR', 'Euro'), ('USD', 'US Dollar'), ('VND', 'Vietnam Dong')], default='USD', editable=False, max_length=3)),
                ('product_price', djmoney.models.fields.MoneyField(decimal_places=2, default=Decimal('0.0'), default_currency='USD', max_digits=10)),
            ],
        ),
        migrations.CreateModel(
            name='ProductOptionImage',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(blank=True, null=True, upload_to='media/%Y/%m/%d/%H/%M/%S/')),
                ('image_link', models.CharField(blank=True, max_length=300, null=True)),
                ('productoption', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='econ.ProductOption')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='ProductPromotion',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('promotion_name', models.CharField(max_length=100)),
                ('promotion_type', models.CharField(choices=[('M', 'Minus'), ('P', 'Percentage'), ('O', 'Offer')], default='P', max_length=1)),
                ('promotion_value', models.FloatField()),
                ('promotion_start', models.DateTimeField(null=True)),
                ('promotion_end', models.DateTimeField(null=True)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='ProductSpecDetail',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('desc', models.CharField(blank=True, max_length=100, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Slug',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('slug', models.SlugField(unique=True)),
                ('object_id', models.PositiveIntegerField()),
                ('content_type', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='contenttypes.ContentType')),
            ],
        ),
        migrations.CreateModel(
            name='Specific',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('specific_name', models.CharField(max_length=50)),
                ('specific_of', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='econ.Cagetory')),
            ],
        ),
        migrations.CreateModel(
            name='SpecificDetail',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('detail_value', models.CharField(blank=True, max_length=50, null=True)),
                ('detail_field', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='econ.Specific')),
            ],
        ),
        migrations.CreateModel(
            name='ProductInfo',
            fields=[
                ('product', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to='econ.Product')),
                ('info', ckeditor.fields.RichTextField(blank=True, null=True)),
            ],
        ),
        migrations.AddField(
            model_name='productspecdetail',
            name='prod',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='econ.Product'),
        ),
        migrations.AddField(
            model_name='productspecdetail',
            name='prod_option',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='econ.ProductOption'),
        ),
        migrations.AddField(
            model_name='productspecdetail',
            name='spec',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='econ.SpecificDetail'),
        ),
        migrations.AddField(
            model_name='productpromotion',
            name='apply_to',
            field=models.ManyToManyField(blank=True, null=True, to='econ.Product'),
        ),
        migrations.AddField(
            model_name='productoption',
            name='prod',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='econ.Product'),
        ),
        migrations.AddField(
            model_name='productimage',
            name='product',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='econ.Product'),
        ),
        migrations.AddField(
            model_name='product',
            name='product_agency',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='econ.Agency'),
        ),
        migrations.AddField(
            model_name='product',
            name='product_branch',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='econ.Brand'),
        ),
        migrations.AddField(
            model_name='product',
            name='product_cagetory',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='econ.Cagetory'),
        ),
        migrations.AddField(
            model_name='agencymember',
            name='inviter',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='membership_invites', to='econ.BaseUser'),
        ),
        migrations.AddField(
            model_name='agencymember',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='econ.BaseUser'),
        ),
        migrations.AddField(
            model_name='agency',
            name='agency_member',
            field=models.ManyToManyField(through='econ.AgencyMember', to='econ.BaseUser'),
        ),
        migrations.AlterUniqueTogether(
            name='specificdetail',
            unique_together=set([('detail_field', 'detail_value')]),
        ),
        migrations.AlterUniqueTogether(
            name='specific',
            unique_together=set([('specific_name', 'specific_of')]),
        ),
        migrations.AlterUniqueTogether(
            name='productspecdetail',
            unique_together=set([('prod', 'prod_option')]),
        ),
    ]
