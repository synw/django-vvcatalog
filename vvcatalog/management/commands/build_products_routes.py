from __future__ import print_function
import os
from django.core.urlresolvers import reverse
from django.core.management.base import BaseCommand, CommandError
from django.conf import settings
from vvcatalog.models import Product

class Command(BaseCommand):
    help = 'Build routes for products'

    def handle(self, *args, **options):
        products = Product.objects.prefetch_related("category").filter(status="published")
        print("Building routes for products ...")
        routes = []
        i = 1
        for product in products:
            slug = product.category.slug
            url = product.get_absolute_url()
            u = "page('"+url+"', function(ctx, next) { app.getProduct('"+product.slug+"') } );"
            routes.append(u)
            print(str(i)+": "+url)
            i += 1
        routes_str = '{# ************ Autogenerated file: do not edit ************ #}\n'+'\n'.join(routes)
        # check directories
        dirpath = settings.BASE_DIR+"/templates/vvcatalog"
        if not os.path.isdir(dirpath) is True:
            print("Creating directory templates/vvcatalog")
            os.makedirs(dirpath)
        dirpath = settings.BASE_DIR+"/templates/vvcatalog/auto"
        if not os.path.isdir(dirpath) is True:
            os.makedirs(dirpath)
            print("Creating directory templates/vvcatalog/auto")
        # update
        filepath=settings.BASE_DIR+"/templates/vvcatalog/auto/products_routes.js"
        print("Updating templates/vvcatalog/auto/products_routes.js")
        #~ write the file
        filex = open(filepath, "w")
        filex.write(routes_str)
        filex.close()
        print("OK: "+str(i-1)+" routes built ")
        return
