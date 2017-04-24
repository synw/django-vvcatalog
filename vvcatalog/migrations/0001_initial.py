# -*- coding: utf-8 -*-
# Generated by Django 1.10.7 on 2017-04-24 12:32
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import filebrowser.fields
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
                ('image', models.ImageField(blank=True, upload_to='brands', verbose_name='Image')),
                ('status', models.CharField(choices=[('pending', 'Pending'), ('published', 'Published'), ('unpublished', 'Unpublished')], default='pending', max_length=20, verbose_name='Status')),
                ('editor', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to=settings.AUTH_USER_MODEL, verbose_name='Posted by')),
            ],
            options={
                'verbose_name_plural': 'Brands',
                'ordering': ['title'],
                'verbose_name': 'Brand',
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
                ('image', filebrowser.fields.FileBrowseField(max_length=200, null=True, verbose_name='Navigation image')),
                ('description', models.TextField(blank=True, verbose_name='Description')),
                ('status', models.CharField(choices=[('pending', 'Pending'), ('published', 'Published'), ('unpublished', 'Unpublished')], default='published', max_length=20, verbose_name='Status')),
                ('content_type', models.CharField(default='category', editable=False, max_length=100)),
                ('url', models.CharField(blank=True, max_length=255, null=True)),
                ('lft', models.PositiveIntegerField(db_index=True, editable=False)),
                ('rght', models.PositiveIntegerField(db_index=True, editable=False)),
                ('tree_id', models.PositiveIntegerField(db_index=True, editable=False)),
                ('level', models.PositiveIntegerField(db_index=True, editable=False)),
                ('editor', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to=settings.AUTH_USER_MODEL, verbose_name='Posted by')),
                ('parent', mptt.fields.TreeForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='children', to='vvcatalog.Category', verbose_name='Parent category')),
            ],
            options={
                'verbose_name_plural': 'Categories',
                'verbose_name': 'Category',
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
                ('civility', models.CharField(choices=[('mr', 'Mr'), ('mm', 'Mme')], default='mr', max_length=60, verbose_name='Title')),
                ('telephone', models.PositiveIntegerField(verbose_name='Phone number')),
                ('company_name', models.CharField(blank=True, max_length=120, verbose_name='Company name')),
                ('email', models.EmailField(max_length=254, verbose_name='Email')),
                ('address', models.TextField(verbose_name='Address')),
                ('extra', jsonfield.fields.JSONField(blank=True, verbose_name='Extra infos')),
                ('content_type', models.CharField(default='catagory', editable=False, max_length=100)),
                ('status', models.CharField(choices=[('pending', 'Pending'), ('published', 'Published'), ('unpublished', 'Unpublished')], default='pending', max_length=20, verbose_name='Status')),
                ('editor', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to=settings.AUTH_USER_MODEL, verbose_name='Posted by')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='User')),
            ],
            options={
                'verbose_name_plural': 'Customers',
                'ordering': ('last_name',),
                'verbose_name': 'Customer',
            },
        ),
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True, null=True, verbose_name='Created')),
                ('edited', models.DateTimeField(auto_now=True, null=True, verbose_name='Edited')),
                ('status', models.CharField(choices=[('pending', 'Pending'), ('confirmed', 'Confirmed'), ('closed', 'Closed'), ('rejected', 'Rejected')], default='pending', max_length=120, verbose_name='Status')),
                ('total', models.FloatField(blank=True, null=True, verbose_name='Total')),
                ('customer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='orders', to='vvcatalog.Customer', verbose_name='Customer')),
                ('editor', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to=settings.AUTH_USER_MODEL, verbose_name='Posted by')),
            ],
            options={
                'verbose_name_plural': 'Orders',
                'ordering': ('-created',),
                'verbose_name': 'Order',
            },
        ),
        migrations.CreateModel(
            name='OrderedProduct',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True, null=True, verbose_name='Created')),
                ('edited', models.DateTimeField(auto_now=True, null=True, verbose_name='Edited')),
                ('quantity', models.PositiveIntegerField(verbose_name='Quantity')),
                ('price_per_unit', models.FloatField(verbose_name='Price per unit')),
                ('editor', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to=settings.AUTH_USER_MODEL, verbose_name='Posted by')),
                ('order', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='+', to='vvcatalog.Order', verbose_name='Order')),
            ],
            options={
                'verbose_name_plural': 'Ordered products',
                'ordering': ('-created', 'order'),
                'verbose_name': 'Ordered product',
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
                ('navimage', filebrowser.fields.FileBrowseField(max_length=200, null=True, verbose_name='Navigation image')),
                ('price', models.FloatField(blank=True, null=True, verbose_name='Price')),
                ('available', models.BooleanField(default=True, verbose_name='Available')),
                ('extra', jsonfield.fields.JSONField(blank=True, verbose_name='Extra infos')),
                ('status', models.CharField(choices=[('pending', 'Pending'), ('published', 'Published'), ('unpublished', 'Unpublished')], default='published', max_length=20, verbose_name='Status')),
                ('content_type', models.CharField(default='product', editable=False, max_length=100)),
                ('url', models.CharField(blank=True, max_length=255, null=True)),
                ('brand', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='vvcatalog.Brand', verbose_name='Brand')),
                ('category', mptt.fields.TreeForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='products', to='vvcatalog.Category', verbose_name='Category')),
                ('editor', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to=settings.AUTH_USER_MODEL, verbose_name='Posted by')),
            ],
            options={
                'verbose_name_plural': 'Products',
                'verbose_name': 'Product',
            },
        ),
        migrations.CreateModel(
            name='ProductImage',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True, null=True, verbose_name='Created')),
                ('edited', models.DateTimeField(auto_now=True, null=True, verbose_name='Edited')),
                ('image', models.ImageField(upload_to='products', verbose_name='Image')),
                ('order', models.PositiveSmallIntegerField(verbose_name='Order')),
                ('editor', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to=settings.AUTH_USER_MODEL, verbose_name='Posted by')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='images', to='vvcatalog.Product', verbose_name='Product')),
            ],
            options={
                'verbose_name_plural': 'Product images',
                'verbose_name': 'Product image',
            },
        ),
        migrations.AddField(
            model_name='orderedproduct',
            name='product',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='ordered', to='vvcatalog.Product', verbose_name='Product'),
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
