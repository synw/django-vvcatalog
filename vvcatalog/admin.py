# -*- coding: utf-8 -*-

from django.utils.translation import ugettext_lazy as _
from django.contrib import admin
from mptt.admin import MPTTModelAdmin
from vvcatalog.models import Product, ProductImage, Category, Brand, Customer, Order, OrderedProduct
from vvcatalog.forms import BrandForm, CategoryForm, ProductForm


#~ ========================================= Inlines ==================================

class ProductImageInline(admin.TabularInline):
    model = ProductImage
    fields = ['image',]
    extra = 0


class OrderdedProductInline(admin.TabularInline):
    model = OrderedProduct
    fields = ['product', 'order', 'quantity', 'price_per_unit']
    readonly_fields = ['order', 'quantity', 'price_per_unit']
    extra = 0

#~ ========================================= Admin classes ==================================

@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ['first_name', 'last_name', 'telephone', 'email', 'user']
    list_select_related = ['user']
    search_fields = ['last_name', 'user__username', 'email', 'telephone']


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    form = ProductForm
    date_hierarchy = 'edited'
    raw_id_fields = ['category','brand']
    prepopulated_fields = {"slug": ("title",)}
    list_display = ['title','brand', 'price', 'category','upc','edited','editor']
    list_filter = ['status', 'created','edited']
    search_fields = ['title','upc','brand__name','category__name','editor__username']
    list_select_related = ['editor','brand','category']
    readonly_fields = ['editor']
    save_on_top = True
    fieldsets = (
        (_(u"Product description"), {
            'classes': ('collapse',),
            'fields': ('description',)
        }),
        (None, {
            'fields': (('title', 'slug'), ('category', 'brand'), ('navimage', 'upc'))
        }),
        (None, {
            'fields': (('price', 'available'),)
        }),
        (None, {
            'fields': ('status', 'short_description')
        }),
        (_(u'Extra infos'), {
            'classes': ('collapse',),
            'fields': ('extra',)
        }),
    )
    
    def form_valid(self, form):
        """This is what's called when the form is valid."""
        instance = form.save(commit=False)
        print "Form valid ----------------"
        return super(ProductAdmin, self).form_valid(form)
    
    def form_invalid(self, form):
        """This is what's called when the form is valid."""
        instance = form.save(commit=False)
        print "Form invalid ----------------"
        return super(ProductAdmin, self).form_invalid(form)
        
    

    def save_model(self, request, obj, form, change):
        if getattr(obj, 'editor', None) is None:
            obj.editor = request.user
        obj.save()
        return
        
    def add_view(self, request, form_url='', extra_context=None):
        self.inlines = [ProductImageInline]
        return super(ProductAdmin, self).add_view(request, form_url, extra_context)

    def change_view(self, request, object_id, form_url='', extra_context=None):
        self.inlines = [ProductImageInline]
        return super(ProductAdmin, self).change_view(request, object_id, form_url, extra_context)
        
        
@admin.register(Category)    
class CategoryAdmin(MPTTModelAdmin):
    form = CategoryForm
    date_hierarchy = 'edited'
    prepopulated_fields = {"slug": ("title",)}
    readonly_fields = ['editor']
    list_display = ['title', 'parent', 'edited', 'editor']
    list_filter = ['status', 'created','edited']
    search_fields = ['title', 'editor__username']
    mptt_level_indent = 30
    save_on_top = True
    list_select_related = ['editor'] 
    fieldsets = (
            (None, {
                'fields': (('title','slug',),)
            }),
            (None, {
                'fields': (('parent','status',), ('image',))
            }),
            (None, {
                'fields': (('description',),)
            }),
            )
    
    def save_model(self, request, obj, form, change):
        if getattr(obj, 'editor', None) is None:
            obj.editor = request.user
        obj.save()


@admin.register(Brand)
class BrandAdmin(admin.ModelAdmin):
    form = BrandForm
    date_hierarchy = 'edited'
    prepopulated_fields = {"slug": ("title",)}
    readonly_fields = ['editor']
    list_display = ['title', 'image', 'status', 'editor','edited']
    list_filter = ['status', 'created','edited']
    search_fields = ['title', 'editor__username']
    list_select_related = ['editor']
    fieldsets = (
            (None, {
                'fields': (('title','slug',),)
            }),
            (None, {
                'fields': ('status','image',),
            }),
            )
    
    def save_model(self, request, obj, form, change):
        if getattr(obj, 'editor', None) is None:
            obj.editor = request.user
        obj.save()
        
@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['created', 'customer', 'total', 'status']
    list_select_related = ['customer']
    search_fields = ['customer__last_name', 'customer__email', 'customer__telephone']
    list_filter = ['status']
    attrs = {'class': 'special', 'size': '40'}
    fields = ['created', 'customer', 'status', 'total']
    readonly_fields = ['created', 'total']
    inlines = [OrderdedProductInline]
    
    def save_model(self, request, obj, form, change):
        if getattr(obj, 'editor', None) is None:
            obj.editor = request.user
        obj.save()
