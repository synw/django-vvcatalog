# -*- coding: utf-8 -*-
# Generated by Django 1.10.7 on 2017-04-18 15:15
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('vvcatalog', '0002_auto_20170418_1450'),
    ]

    operations = [
        migrations.AddField(
            model_name='category',
            name='content_type',
            field=models.CharField(default='category', editable=False, max_length=100),
        ),
        migrations.AddField(
            model_name='customer',
            name='content_type',
            field=models.CharField(default='catagory', editable=False, max_length=100),
        ),
        migrations.AddField(
            model_name='product',
            name='content_type',
            field=models.CharField(default='product', editable=False, max_length=100),
        ),
    ]