# -*- coding: utf-8 -*-

from django.conf.urls import url, include
from vvcatalog.views import categoryIndexView, categoryView, productsInCatView, productDetailView, \
isAuthenticated, SetCart, CustomerUpdateFormView, CustomerFormView, ConfirmOrderView, \
CustomerFormDispatcher, CustomerFormUpdateDispatcher, CreateOrderView, OrderError, OrderOk
from vv.views import IndexView as VVIndex

urlpatterns = [
    url(r'^set_cart/$', SetCart.as_view(), name="set-cart"),
    url(r'^x/customer/dispatch/update/$', CustomerFormUpdateDispatcher.as_view(), name="customer-form-update-dispatcher"),
    url(r'^x/customer/dispatch/$', CustomerFormDispatcher.as_view(), name="customer-form-dispatcher"),
    url(r'^x/customer/$', CustomerFormView.as_view(), name="customer-form"),
    url(r'^customer/update/(?P<pk>[0-9]+)/$', CustomerUpdateFormView.as_view(), name="update-customer-form"),
    url(r'^x/is_authenticated/$', isAuthenticated, name="is-authenticated"),
    url(r'^x/confirm/$', ConfirmOrderView.as_view(), name="confirm-order"),
    url(r'^x/order/create/$', CreateOrderView.as_view(), name="create-order"),
    url(r'^x/order/ok/$', OrderOk.as_view(), name="order-ok"),
    url(r'^x/order/error/$', OrderError.as_view(), name="order-error"),
    url(r'^', VVIndex.as_view(), name="category-index"),
    ]
