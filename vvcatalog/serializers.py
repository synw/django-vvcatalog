# -*- coding: utf-8 -*-

from rest_framework import serializers
from vvcatalog.models import Category, Product, Customer


class CategorySerializer(serializers.ModelSerializer):
    url = serializers.SerializerMethodField()
    content_type = serializers.SerializerMethodField()
    
    class Meta:
        model = Category
        fields = ('title', "slug", "description", "image", "url", "content_type")
        read_only_fields = fields
        
    def get_url(self, obj):
        return obj.get_absolute_url()
    
    def get_content_type(self, obj):
        return "category"
 
    
class CustomerSerializer(serializers.ModelSerializer):
    content_type = serializers.SerializerMethodField()

    class Meta:
        model = Customer
        fields = ('first_name', "last_name", "civility", "telephone", "email", "address", "content_type")
        read_only_fields = fields
        
    def get_content_type(self, obj):
        return "customer"


class ProductSerializer(serializers.ModelSerializer):
    content_type = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = ('title', "slug", "description", "short_description", "upc", "navimage", "images", "brand", "category",
                   "price", "extra", "content_type")
        read_only_fields = fields
        
    def get_content_type(self, obj):
        return "product"
