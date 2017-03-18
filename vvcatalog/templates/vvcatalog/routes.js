{% load i18n %}
page("/catalog/customer/", function(ctx, next) { app.loadCustomerForm("{% url 'customer-form' %}") } );
page("/catalog/confirm/sum/", function(ctx, next) { app.acceptSummary() } );
{% include "vvcatalog/auto/categories_routes.js" %}
{% include "vvcatalog/auto/products_routes.js" %}