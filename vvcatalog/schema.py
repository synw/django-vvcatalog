# -*- coding: utf-8 -*-

import graphene
from graphene_django.types import DjangoObjectType
from graphene_django.filter import DjangoFilterConnectionField
from graphene import relay
from vvcatalog.models import Product, Category


class CategoryNode(DjangoObjectType):
    class Meta:
        model = Category
        only_fields = ("slug", "title", "image", "products", "content_type", 'children', "url")
        filter_fields = {
            'slug' : ['exact'],
            'title' : ['exact', 'icontains', 'istartswith'],
            'children' : ['exact', 'icontains', 'istartswith']
            }
        interfaces = (relay.Node, )


class ProductNode(DjangoObjectType):
    class Meta:
        model = Product
        only_fields = ("content_type", "slug", "title", "navimage", "images", "category", 'price', "url")
        filter_fields = ['slug', 'id', 'title', 'category']
        interfaces = (relay.Node, )


class Query(graphene.AbstractType):
    all_categories = DjangoFilterConnectionField(CategoryNode)
    category = graphene.Field(CategoryNode,
                              id=graphene.Int(),
                              slug=graphene.String())
    product = graphene.Field(ProductNode,
                                id=graphene.Int(),
                                slug=graphene.String())

    def resolve_all_categories(self, args, context, info):
        return Category.objects.filter(status="published")

    def resolve_category(self, args, context, info):
        slug = args.get('slug')
        if slug is not None:
            #print str(context.session)
            return Category.objects.filter(slug=slug).prefetch_related('products', 'children')[0]

        return None

    def resolve_product(self, args, context, info):
        slug = args.get('slug')
        if slug is not None:
            return Product.objects.get(slug=slug)

        return None
