# -*- coding: utf-8 -*-

from django.core.urlresolvers import reverse
from django.core.management import call_command
from django.db import models
from django.utils import formats
from django.utils.translation import ugettext_lazy as _
from mptt.models import TreeForeignKey, MPTTModel
from jsonfield import JSONField
from vvcatalog.conf import USER_MODEL, STATUSES, CIVILITIES, ORDER_STATUSES


class BaseModel(models.Model):
    editor = models.ForeignKey(USER_MODEL, null=True, blank=True, related_name='+', on_delete=models.SET_NULL, verbose_name=_(u'Posted by'))
    created = models.DateTimeField(editable=False, null=True, blank=True, auto_now_add=True, verbose_name=_(u'Created'))
    edited = models.DateTimeField(editable=False, null=True, blank=True, auto_now=True, verbose_name=_(u'Edited'))
    
    class Meta:
        abstract = True
        
        
class Customer(BaseModel):
    first_name = models.CharField(max_length=120, verbose_name=_(u'First name'))
    last_name = models.CharField(max_length=120, verbose_name=_(u'Last name'))
    civility = models.CharField(max_length=60, verbose_name=_(u'Title'), choices=CIVILITIES, default=CIVILITIES[0][0])
    telephone = models.PositiveIntegerField(verbose_name=_(u'Phone number'))
    company_name = models.CharField(max_length=120, blank=True, verbose_name=_(u'Company name'))
    email = models.EmailField(verbose_name=_(u'Email'))
    address = models.TextField(verbose_name=_(u'Address'))
    user = models.OneToOneField(USER_MODEL, verbose_name=_(u'User') )
    extra = JSONField(blank=True, verbose_name=_(u'Extra infos'))
    status = models.CharField(max_length=20, verbose_name=_(u'Status'), choices=STATUSES, default=STATUSES[0][0])
    
    class Meta:
        verbose_name=_(u'Customer')
        verbose_name_plural = _(u'Customers')
        ordering = ('last_name',)
        unique_together = ('first_name', 'last_name')

    def __unicode__(self):
        return unicode(self.first_name+' '+self.last_name)
    
    def get_absolute_url(self):
        return "/catalog/customer/"

    @property
    def telephone_formated(self):
        return '%s %s %s %s' %(self.telephone[0:2],self.telephone[2:4],self.telephone[4:6],self.telephone[6:8])
    
    def get_civility(self):
        for civ in CIVILITIES:
            if civ[0] == self.civility:
                return civ[1]
        return self.civility


class Brand(BaseModel):
    slug = models.SlugField(max_length=25, unique=True)
    title = models.CharField(max_length=255, verbose_name=_(u'Title'))
    image = models.ImageField(blank=True, upload_to='brands', verbose_name=_(u'Image'))
    status = models.CharField(max_length=20, verbose_name=_(u'Status'), choices=STATUSES, default=STATUSES[0][0])
    
    class Meta:
        verbose_name=_(u'Brand')
        verbose_name_plural = _(u'Brands')
        ordering = ['title']

    def __unicode__(self):
        return unicode(self.title)
    

class Category(MPTTModel, BaseModel):
    slug = models.SlugField(max_length=25, unique=True)
    title = models.CharField(max_length=255, verbose_name=_(u'Title'))
    parent = TreeForeignKey('self', null=True, blank=True, related_name=u'children', verbose_name=_(u'Parent category'))
    image = models.ImageField(null=True, upload_to='categories', verbose_name=_(u"Navigation image"))
    description = models.TextField(blank=True, verbose_name=_(u'Description'))
    status = models.CharField(max_length=20, verbose_name=_(u'Status'), choices=STATUSES, default=STATUSES[1][0])
    
    class Meta:
        verbose_name=_(u'Category')
        verbose_name_plural = _(u'Categories')

    def __unicode__(self):
        return unicode(self.title)
    
    def get_absolute_url(self):
        index = reverse("category-index")
        url = index+"category/"+self.slug+"/"
        return url
    
    def update_routes(self):
        call_command('build_categories_routes', verbosity=0)
        return
    
    def save(self, *args, **kwargs):
        super(Category, self).save(*args, **kwargs)
        self.update_routes()
        return
    
    def delete(self, *args, **kwargs):
        super(Category, self).delete(*args, **kwargs)
        self.update_routes()
        return
    
    @property
    def url(self):
        return self.get_absolute_url()


class Product(BaseModel):
    slug = models.SlugField(max_length=25, unique=True)
    title = models.CharField(max_length=255, verbose_name=_(u'Title'))
    #~ base content
    short_description = models.TextField(blank=True, verbose_name=_(u'Short description'))
    description = models.TextField(blank=True, verbose_name=_(u'Long description'))
    upc = models.CharField(null=True, max_length=30, verbose_name=_(u'Universal Product Code'))
    navimage = models.ImageField(null=True, upload_to='products/nav/', verbose_name=_(u'Navigation image'))
    #~ external keys
    brand = models.ForeignKey(Brand, blank=True, null=True, on_delete=models.PROTECT, verbose_name=_(u'Brand'))
    category = TreeForeignKey(Category, verbose_name=_(u'Category'))
    #~ prices
    price = models.FloatField(null=True, blank=True, verbose_name=_(u'Price'))
    available = models.BooleanField(default=True, verbose_name=_(u'Available'))
    #~ extra info
    extra = JSONField(blank=True, verbose_name=_(u'Extra infos'))
    status = models.CharField(max_length=20, verbose_name=_(u'Status'), choices=STATUSES, default=STATUSES[1][0])
    
    class Meta:
        verbose_name=_(u'Product')
        verbose_name_plural =_( u'Products')
        #if USE_PRICES is True:
        #    ordering = ('price', 'name','created')
        #ordering = ('name','created')
        order_with_respect_to = 'category'

    def __unicode__(self):
        return unicode(self.title)
    
    def get_absolute_url(self):
        index = reverse("category-index")
        url = index+"product/"+self.slug+"/"
        return url
    
    def update_routes(self):
        call_command('build_products_routes', verbosity=0)
        return
    
    def save(self, *args, **kwargs):
        super(Product, self).save(*args, **kwargs)
        self.update_routes()
        return
    
    def delete(self, *args, **kwargs):
        super(Product, self).delete(*args, **kwargs)
        self.update_routes()
        return

    
    
class ProductImage(BaseModel):
    image = models.ImageField(upload_to='products', verbose_name=_(u'Image'))
    #~ external key
    product = models.ForeignKey(Product, related_name="images", verbose_name=_(u'Product'))
    order = models.PositiveSmallIntegerField(verbose_name=_(u'Order'))
    
    class Meta:
        verbose_name=_(u'Product image')
        verbose_name_plural = _(u'Product images')

    def __unicode__(self):
        return unicode(self.image.url)
    
class Order(BaseModel):
    customer = models.ForeignKey(Customer, related_name='orders', verbose_name=_(u'Customer'))
    status = models.CharField(max_length=120, verbose_name=_(u'Status'), choices=ORDER_STATUSES, default=ORDER_STATUSES[0][0])
    total = models.FloatField(null=True, blank=True, verbose_name=_(u'Total'))

    class Meta:
        verbose_name=_(u'Order')
        verbose_name_plural = _(u'Orders')
        ordering = ('-created',)

    def __unicode__(self):
        date = formats.date_format(self.created, "SHORT_DATETIME_FORMAT")
        return unicode(date+' - '+str(self.total)+' - '+self.status)


class OrderedProduct(BaseModel):
    product = models.ForeignKey(Product, null=True, related_name='ordered', on_delete=models.SET_NULL, verbose_name=_(u'Product'))
    order = models.ForeignKey(Order, related_name='+', verbose_name=_(u'Order'))
    quantity = models.PositiveIntegerField(verbose_name=_(u'Quantity'))
    price_per_unit = models.FloatField(verbose_name=_(u'Price per unit'))
    
    class Meta:
        verbose_name=_(u'Ordered product')
        verbose_name_plural = _(u'Ordered products')
        ordering = ('-created', 'order')

    def __unicode__(self):
        date = formats.date_format(self.created, "SHORT_DATETIME_FORMAT")
        return unicode(date)
