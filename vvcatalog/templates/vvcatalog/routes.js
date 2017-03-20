{% load i18n %}
page("/catalog/customer/", function(ctx, next) { app.loadCustomerForm(ctx) } );
//page("/catalog/customer/goupdate/", function(ctx, next) { app.updateCustomerForm() } );
page("/catalog/confirm/", function(ctx, next) { app.confirmInfos() } );
page("/catalog/confirm/sum/", function(ctx, next) { app.acceptSummary() } );
{% include "vvcatalog/auto/categories_routes.js" %}
{% include "vvcatalog/auto/products_routes.js" %}