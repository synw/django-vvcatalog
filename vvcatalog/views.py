# -*- coding: utf-8 -*-

import json
from django.core.urlresolvers import reverse
from django.views.generic import CreateView, TemplateView, View
from django.views.generic.edit import UpdateView
from django.views.generic.base import RedirectView
from django.http import HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404, redirect, Http404
from django.conf import settings
from django.template import loader, RequestContext
from rest_framework.renderers import JSONRenderer
from rest_framework.permissions import IsAuthenticated
from braces.views import LoginRequiredMixin
from vvcatalog.serializers import CategorySerializer, ProductSerializer, CustomerSerializer
from vvcatalog.models import Category, Product, Customer, Order, OrderedProduct
from vvcatalog.forms import CustomerForm


class JSONResponse(HttpResponse):

    def __init__(self, data, **kwargs):
        content = JSONRenderer().render(data)
        kwargs['content_type'] = 'application/json'
        super(JSONResponse, self).__init__(content, **kwargs)
        
        
class OrderOk(LoginRequiredMixin, TemplateView):
    template_name = 'vvcatalog/order/post_success.html'
    

class OrderError(LoginRequiredMixin, TemplateView):
    template_name = 'vvcatalog/order/post_error.html'


class CreateOrderView(LoginRequiredMixin, TemplateView):
    template_name = 'vvcatalog/order/create.html'
    login_url = settings.LOGIN_URL
    
    def post(self, request, *args, **kwargs):
        resp = json.loads(self.request.body)
        try:
            customer = Customer.objects.get(user=self.request.user)
        except:
            JsonResponse({"ok":0})
        final = []
        slugs = []
        total = 0
        for el in resp["cart"]:
            slug = el["product"]["slug"]
            price = el["product"]["price"]
            num = el["num"]
            subt = num*price
            total = total+subt
            final.append((slug, price, num))
            slugs.append(slug)
        #print str(products)
        order = Order.objects.create(customer=customer, total=total)
        products = Product.objects.filter(slug__in=slugs)
        for el in final:
            product = products.filter(slug=el[0])[0]
            OrderedProduct.objects.create(product=product, order=order, price_per_unit=el[1], quantity=el[2])
        return JsonResponse({"ok":1})


class CustomerFormDispatcher(RedirectView):
    
    def get_redirect_url(self, *args, **kwargs):
        super(CustomerFormDispatcher, self).get_redirect_url(*args, **kwargs)
        if Customer.objects.filter(user=self.request.user).exists():
            return "/catalog/confirm/"
        else:
            return "/catalog/customer/"


class CustomerFormUpdateDispatcher(RedirectView):
    
    def get_redirect_url(self, *args, **kwargs):
        super(CustomerFormUpdateDispatcher, self).get_redirect_url(*args, **kwargs)
        try:
            customer = Customer.objects.get(user=self.request.user)
            return "/catalog/customer/update/"+str(customer.pk)+"/"
        except Customer.DoesNotExist:
            return "/catalog/customer/"  


class CustomerUpdateFormView(LoginRequiredMixin, UpdateView):
    model = Customer
    form_class = CustomerForm
    template_name = 'vvcatalog/order/customer_update_form.html'
    
    def get_login_url(self):
        return settings.LOGIN_URL+'?next='+reverse('customer-update-form')
    
    def form_valid(self, form, **kwargs):
        if self.request.method == "POST":
            obj = form.save(commit=False)
            obj.user = self.request.user
        else: 
            raise Http404
        return super(CustomerUpdateFormView, self).form_valid(form)
    
    def get_success_url(self):
        return "/catalog/confirm/"
    

class CustomerFormView(LoginRequiredMixin, CreateView):
    model = Customer
    form_class = CustomerForm
    template_name = 'vvcatalog/order/customer_form.html'
    
    def dispatch(self, request, *args, **kwargs):
        if not self.request.user.is_anonymous:      
            if Customer.objects.filter(user=request.user).exists():
                url = "/catalog/confirm/"
                return redirect(url)
        return super(CustomerFormView, self).dispatch(request, *args, **kwargs)
    
    def get_login_url(self):
        return settings.LOGIN_URL+'?next='+reverse('customer-form')
    
    def get_success_url(self):
        return "/catalog/confirm/"
    
    def form_valid(self, form, **kwargs):
        if self.request.method == "POST":
            obj = form.save(commit=False)
            obj.user = self.request.user
        else: 
            raise Http404
        return super(CustomerFormView, self).form_valid(form)


class ConfirmOrderView(LoginRequiredMixin, TemplateView):
    template_name = 'vvcatalog/order/confirm_order.html'
    
    def get_login_url(self):
        return settings.LOGIN_URL+'?next='+reverse('confirm-order')
    
    def get_context_data(self, **kwargs):
        context = super(ConfirmOrderView, self).get_context_data(**kwargs)
        context['customer'] = get_object_or_404(Customer, user=self.request.user)
        return context

"""
def confirmOrderView(request, slug):
    if request.user.is_anonymous is True:
        return redirect("/catalog/")
    try:
        customer = Customer.objects.get(user=request.user)
    except Customer.DoesNotExist:
        
    data = {"customer": customer.pk}
    if exists:
        data = {"exists": "true"}
    return JsonResponse(data)
"""

def categoryIndexView(request):
    q = Category.objects.filter(level__lte=0, status="published")
    serializer = CategorySerializer(q, many=True)
    return JSONResponse(serializer.data)

def categoryView(request, slug):
    current_category=get_object_or_404(Category, slug=slug)
    last_level=current_category.level+1
    q = descendants = current_category.get_descendants().filter(level__lte=last_level, status="published")
    if len(descendants) == 0:
        q = Product.objects.filter(category=current_category, status="published")
        serializer = ProductSerializer(q, many=True)
    else:
        serializer = CategorySerializer(q, many=True)
    return JSONResponse(serializer.data)

def productsInCatView(request, slug):
    category = get_object_or_404(Category.objects, slug=slug, status="published")
    q = Product.objects.filter(category=category, status="published")
    serializer = ProductSerializer(q, many=True)
    return JSONResponse(serializer.data)

def productDetailView(request, slug):
    q = get_object_or_404(Product.objects.prefetch_related('images','brand'), slug=slug, status="published")
    serializer = ProductSerializer(q)
    return JSONResponse(serializer.data)


class SetCart(RedirectView):
    pattern_name = "set-cart"
    permanent = True
    query_string = True
    
    def __init__(self, *args, **kwargs):
        super(SetCart, self).__init__(**kwargs)
        
    def get_redirect_url(self, *args, **kwargs):
        # place cart in session
        print "GET "+str(self.request.GET)
        return super(SetCart, self).get_redirect_url(*args, **kwargs)


def isAuthenticated(request):
    response = {}
    response["is_authenticated"] = False
    if request.user.is_authenticated:
        response["is_authenticated"] = True
    payload = json.dumps(response)
    return HttpResponse(payload, content_type="application/json")
