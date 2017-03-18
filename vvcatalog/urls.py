# -*- coding: utf-8 -*-

from django.conf.urls import url, include
from vvcatalog.views import categoryIndexView, categoryView, productsInCatView, productDetailView, \
isAuthenticated, SetCart, PostOrderView, CustomerUpdateFormView, CustomerFormView, ConfirmOrderView
from vv.views import IndexView as VVIndex

urlpatterns = [
    url(r'^set_cart/$', SetCart.as_view(), name="set-cart"),
    url(r'^x/customer/$', CustomerFormView.as_view(), name="customer-form"),
    url(r'^post/$', PostOrderView.as_view(), name="post-order"),
    url(r'^customer/update/(?P<pk>[0-9]+)/$', CustomerUpdateFormView.as_view(), name="update-customer-form"),
    url(r'^x/is_authenticated/$', isAuthenticated, name="is-authenticated"),
    #url(r'^category/(?P<slug>[-_\w]+)/$', IndexView.as_view(), name="category-detail"),
    #url(r'^products/(?P<slug>[-_\w]+)/$', IndexView.as_view(), name="products-in-cat"),
    url(r'^x/category/(?P<slug>[-_\w]+)/$', categoryView, name="category-detail-api"),
    url(r'^x/product/(?P<slug>[-_\w]+)/$', productDetailView, name="product-detail-api"),
    url(r'^x/products/(?P<slug>[-_\w]+)/$', productsInCatView, name="products-in-cat-api"),
    url(r'^x/$', categoryIndexView, name="category-index-api"),
    url(r'^x/confirm/$', ConfirmOrderView.as_view(), name="confirm-order"),
    url(r'^', VVIndex.as_view(), name="category-index"),
    ]
