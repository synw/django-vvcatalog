{% load i18n %}
InitCatalog: function() {
	var stored_cart = store.get("cart") || [];
	if (stored_cart.length > 0) {
		this.cart = stored_cart;
		this.ShowToggleBtn();
	}
},
AddToCart: function(product) {
	var cart_item = this.getCartItem(product);
	if (cart_item != null) {;
		cart_item.num = cart_item.num+1;
		cart_item.price = cart_item.price+product.price;
	} else {
		var cart_item = this.createCartItem(product);
		this.cart.push(cart_item);
		store.remove("cart");
		store.set("cart", this.cart);
	}
},
RemoveFromCart: function(cart_item) {
	if (cart_item.num < 2) {
		this.cart.pop(cart_item);
	} else {
		cart_item.num = cart_item.num-1;
		cart_item.price = cart_item.price-cart_item.product.price;
	}
	store.remove("cart");
	store.set("cart", this.cart);
},
AddPop: function(product) {
	var slider = document.getElementById('cart');
	var is_open = slider.classList.contains('slide-in');
	if (is_open != true) {
		slider.setAttribute('class', "slide-in");
	}
	this.ShowToggleBtn();
	this.AddToCart(product);
},
ToggleCart: function() {
	//document.getElementById('cart').classList.toggle('slide-out');
	//document.getElementById('cart').classList.toggle('slide-out');
	var slider = document.getElementById('cart');
	var toggle = document.getElementById('toggle');
	var isOpen = slider.classList.contains('slide-in');
	slider.setAttribute('class', isOpen ? 'slide-out' : 'slide-in');
},
ShowToggleBtn: function() {
	document.getElementById('btn-open').style.display="block";
},
HideToggleBtn: function() {
	document.getElementById('btn-open').style.display="none";
},
HideCart: function() {
	this.ToggleCart();
    this.HideToggleBtn();
},
listCats: function(resturl, current_category) {
	promise.get(resturl,{},{"Accept":"application/json"}).then(function(error, data, xhr) {
	    if (error) {console.log('Error ' + xhr.status);return;}    
	    data = JSON.parse(data);
	    app.flush();
	    // check content type
	    if (data.length > 0) {
	    	app.noCats = "hidden";
		    content_type = data[0].content_type;
		    if (content_type == "product") {
		    	app.categories = [];
		    	app.products = data;
		    	app.activate(["products"]);
		    } else {
		    	app.products = [];
		    	app.categories = data;
		    	app.activate(["categories"]);
		    }
	    } else {
	    	app.categories = [];
	    	app.products = [];
	    	app.noCats = "visible";
	    }
	    cc = current_category;
	    if (cc == "") {
	    	cc = "{% trans 'Categories' %}"
	    }
 	    app.current_category = cc;
	    top.document.title = "{% trans 'Categories' %}";
	});
	return
},
printProd: function(resturl) {
	promise.get(resturl,{},{"Accept":"application/json"}).then(function(error, data, xhr) {
	    if (error) {console.log('Error ' + xhr.status);return;}
	    app.flush();
	    data = JSON.parse(data);
	    app.products = data;
	    app.activate(["products"]);
	    top.document.title = "{% trans 'Products' %}";
	});
	return
},
createCartItem: function(product) {
	var cart_item = {"product":product, "num":1, "price":product.price, "slug":product.slug};
	return cart_item
},
getCartItem: function(product) {
	for (i=0;i<this.cart.length;i++) {
		if (this.cart[i].product.slug == product.slug) {
			return this.cart[i]
		}
	}
	return null
},
HandleOrder: function() {
	var resturl = "{% url 'is-authenticated' %}";
	promise.get(resturl,{}, {"Accept":"application/json"}).then(function(error, data, xhr) {
	    if (error) {console.log('Error ' + xhr.status);return;}
	    data = JSON.parse(data);
	    if (data.is_authenticated == true) {
	    	self.location.href="{% url 'customer-form' %}#top"
	    } else {
	    	document.getElementById('login').style.display="block";
	    	document.getElementById('order').style.display="none";
	    }
	});
},
loadCustomerForm: function() {
	this.ToggleCart();
	this.flush();
	this.activate(["customer_form", "summary"]);
	var resturl = "{% url 'customer-form' %}";
	promise.get(resturl,{}, {"Accept":"application/json"}).then(function(error, data, xhr) {
	    if (error) {console.log('Error ' + xhr.status);return;}
	    app.customerForm = data;
	});
},
acceptSummary: function() {
	console.log("SUM");
	this.pushActivate(["delivery"]);
	//window.location.hash="#delivery";
},
goAuth: function(from) {
	var resturl = "{% url 'set-cart' %}";
	resturl = resturl+"?"+encodeCartData();
	resturl = resturl+"from="+from;
	self.location.href = resturl;
},
gotoContent: function() {
	self.location.href="#top";
},
encodeCartData: function() {
	var str = "";
	for (i=0;i<app.cart.length;i++) {
		var item = app.cart[i];
		str = str+item.slug+"="+item.num+"&";
	}
	return str
},
