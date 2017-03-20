{% load i18n %}
page("/catalog/customer/", function(ctx, next) { app.loadCustomerForm(ctx) } );
page("/catalog/confirm/", function(ctx, next) { app.confirmInfos() } );
page("/catalog/order/ok/", function(ctx, next) { app.loadChunk("/catalog/x/order/ok/", "{% trans 'Order sent' %}") } );
page("/catalog/order/error/", function(ctx, next) { app.orderError() } );
{% include "vvcatalog/auto/categories_routes.js" %}
{% include "vvcatalog/auto/products_routes.js" %}