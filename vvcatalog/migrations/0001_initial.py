# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-03-13 09:59
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import jsonfield.fields
import mptt.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Brand',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True, null=True, verbose_name='Created')),
                ('edited', models.DateTimeField(auto_now=True, null=True, verbose_name='Edited')),
                ('slug', models.SlugField(max_length=25, unique=True)),
                ('title', models.CharField(max_length=255, verbose_name='Title')),
                ('image', models.ImageField(blank=True, upload_to=b'brands', verbose_name='Image')),
                ('status', models.CharField(choices=[(b'pending', 'Pending'), (b'published', 'Published'), (b'unpublished', 'Unpublished')], default=b'pending', max_length=20, verbose_name='Status')),
                ('editor', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to=settings.AUTH_USER_MODEL, verbose_name='Posted by')),
            ],
            options={
                'ordering': ['title'],
                'verbose_name': 'Brand',
                'verbose_name_plural': 'Brands',
            },
        ),
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True, null=True, verbose_name='Created')),
                ('edited', models.DateTimeField(auto_now=True, null=True, verbose_name='Edited')),
                ('slug', models.SlugField(max_length=25, unique=True)),
                ('title', models.CharField(max_length=255, verbose_name='Title')),
                ('image', models.ImageField(null=True, upload_to=b'categories', verbose_name='Navigation image')),
                ('description', models.TextField(blank=True, verbose_name='Description')),
                ('status', models.CharField(choices=[(b'pending', 'Pending'), (b'published', 'Published'), (b'unpublished', 'Unpublished')], default=b'published', max_length=20, verbose_name='Status')),
                ('lft', models.PositiveIntegerField(db_index=True, editable=False)),
                ('rght', models.PositiveIntegerField(db_index=True, editable=False)),
                ('tree_id', models.PositiveIntegerField(db_index=True, editable=False)),
                ('level', models.PositiveIntegerField(db_index=True, editable=False)),
                ('editor', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to=settings.AUTH_USER_MODEL, verbose_name='Posted by')),
                ('parent', mptt.fields.TreeForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='children', to='vvcatalog.Category', verbose_name='Parent category')),
            ],
            options={
                'verbose_name': 'Category',
                'verbose_name_plural': 'Categories',
            },
        ),
        migrations.CreateModel(
            name='Customer',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True, null=True, verbose_name='Created')),
                ('edited', models.DateTimeField(auto_now=True, null=True, verbose_name='Edited')),
                ('first_name', models.CharField(max_length=120, verbose_name='First name')),
                ('last_name', models.CharField(max_length=120, verbose_name='Last name')),
                ('civility', models.CharField(choices=[(b'mr', 'Mr'), (b'mm', 'Mme')], default=b'mr', max_length=60, verbose_name='Title')),
                ('telephone', models.PositiveIntegerField(verbose_name='Phone number')),
                ('company_name', models.CharField(blank=True, max_length=120, verbose_name='Company name')),
                ('email', models.EmailField(max_length=254, verbose_name='Email')),
                ('address', models.TextField(verbose_name='Address')),
                ('extra', jsonfield.fields.JSONField(blank=True, verbose_name='Extra infos')),
                ('status', models.CharField(choices=[(b'pending', 'Pending'), (b'published', 'Published'), (b'unpublished', 'Unpublished')], default=b'pending', max_length=20, verbose_name='Status')),
                ('editor', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to=settings.AUTH_USER_MODEL, verbose_name='Posted by')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='User')),
            ],
            options={
                'ordering': ('last_name',),
                'verbose_name': 'Customer',
                'verbose_name_plural': 'Customers',
            },
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True, null=True, verbose_name='Created')),
                ('edited', models.DateTimeField(auto_now=True, null=True, verbose_name='Edited')),
                ('slug', models.SlugField(max_length=25, unique=True)),
                ('title', models.CharField(max_length=255, verbose_name='Title')),
                ('short_description', models.TextField(blank=True, verbose_name='Short description')),
                ('description', models.TextField(blank=True, verbose_name='Long description')),
                ('upc', models.CharField(max_length=30, null=True, verbose_name='Universal Product Code')),
                ('navimage', models.ImageField(null=True, upload_to=b'products/nav/', verbose_name='Navigation image')),
                ('price', models.FloatField(blank=True, null=True, verbose_name='Price')),
                ('available', models.BooleanField(default=True, verbose_name='Available')),
                ('extra', jsonfield.fields.JSONField(blank=True, verbose_name='Extra infos')),
                ('status', models.CharField(choices=[(b'pending', 'Pending'), (b'published', 'Published'), (b'unpublished', 'Unpublished')], default=b'published', max_length=20, verbose_name='Status')),
                ('brand', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='vvcatalog.Brand', verbose_name='Brand')),
                ('category', mptt.fields.TreeForeignKey(on_delete=django.db.models.deletion.CASCADE, to='vvcatalog.Category', verbose_name='Category')),
                ('editor', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to=settings.AUTH_USER_MODEL, verbose_name='Posted by')),
            ],
            options={
                'verbose_name': 'Product',
                'verbose_name_plural': 'Products',
            },
        ),
        migrations.CreateModel(
            name='ProductImage',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True, null=True, verbose_name='Created')),
                ('edited', models.DateTimeField(auto_now=True, null=True, verbose_name='Edited')),
                ('image', models.ImageField(upload_to=b'products', verbose_name='Image')),
                ('order', models.PositiveSmallIntegerField(verbose_name='Order')),
                ('editor', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to=settings.AUTH_USER_MODEL, verbose_name='Posted by')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='images', to='vvcatalog.Product', verbose_name='Product')),
            ],
            options={
                'verbose_name': 'Product image',
                'verbose_name_plural': 'Product images',
            },
        ),
        migrations.AlterOrderWithRespectTo(
            name='product',
            order_with_respect_to='category',
        ),
        migrations.AlterUniqueTogether(
            name='customer',
            unique_together=set([('first_name', 'last_name')]),
        ),
    ]
