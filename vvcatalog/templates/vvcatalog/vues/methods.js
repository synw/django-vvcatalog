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
getRootCats: function() {
	q = 'query{rootCategories{edges{node{title,image,url}}}}';
	function error(err) {
		console.log("An error has occured", err);
	}
	function action(data) {
		app.flush();
		app.products = [];
		var cats = [];
		var rawcats = data.rootCategories.edges;
		i=0;
		while (i<rawcats.length) {
			var cat = rawcats[i].node;
			cat.image = "/media/"+cat.image;
			cats.push(cat);
			i++
		}
  		app.categories = cats;
  		app.activate(["categories"]);
	}
	runQuery(q, action, error, true);
},
getCategories: function(slug) {
	var q = 'query{category(slug:"'+slug+'"){slug,title,children{edges{node{url,slug,title,image}}}}}';
	function error(err) {
		console.log("An error has occured", err);
	}
	function action(data) {
		app.flush();
		app.products = [];
		var cats = [];
		var rawcats = data.category.children.edges;
		i=0;
		while (i<rawcats.length) {
			var cat = rawcats[i].node;
			cat.image = "/media/"+cat.image;
			cats.push(cat);
			i++
		}
  		app.categories = cats;
  		app.activate(["categories"]);
	}
	runQuery(q, action, error, true);
	return
},
getProducts: function(slug) {
	var q = 'query{category(slug:"'+slug+'"){slug,title,products{edges{node{slug,title,navimage}}}}}';
	function error(err) {
		console.log("An error has occured", err);
	}
	function action(data) {
		var products = [];
		var prods = data.category.products.edges;
		i=0;
		while (i<prods.length) {
			var prod = prods[i].node;
			prod.navimage = "/media/"+prod.navimage;
			products.push(prod);
			i++
		}
		app.flush();
		app.products = products
  		app.activate(["products"]);
	}
	runQuery(q, action, error, true);
	return
},
getProduct: function(resturl) {
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
	    	page("{% url 'customer-form-dispatcher' %}");
	    } else {
	    	document.getElementById('login').style.display="block";
	    	document.getElementById('order').style.display="none";
	    }
	});
},
postOrder: function() {
	post_order();
},
cancelOrder: function() {
	this.cart = [];
	store.remove("cart");
	store.set("cart", this.cart);
	self.location.href="#top";
	page("/catalog/");
},
goAuth: function goAuth(from) {
	if (from == "login") {
		self.location.href = "{% url 'account_login' %}?next=/catalog/customer/";
	} else if (from == "register") {
		self.location.href = "{% url 'account_signup' %}?next=/catalog/customer/";
	}
	
},
loadCustomerForm: function(ctx) {
	this.flush();
	this.activate(["customer_form", "summary"]);
	var resturl = "{% url 'customer-form' %}";
	promise.get(resturl,{}, {"Accept":"application/json"}).then(function(error, data, xhr) {
	    if (error) {console.log('Error ' + xhr.status);return;}
	    app.customerForm = data;
	});
},
confirmInfos: function() {
	this.activate(["customer_form", "summary", "confirmOrder"]);
	this.customerFormPosted = true;
	var resturl = "{% url 'confirm-order' %}";
	promise.get(resturl,{}, {"Accept":"application/json"}).then(function(error, data, xhr) {
	    if (error) {console.log('Error ' + xhr.status);return;}
	    app.customerForm = data;
	});
},
acceptSummary: function() {
	this.sumAccepted = true;
	this.delivery = true;
	this.activate(["sumAccepted", "customer_form", "summary", "confirmOrder"]);
},
acceptDelivery: function() {
	this.deliveryAccepted = true;
	this.delivery = false;
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
getItemPrice: function(price, num) {
	return price*num
},
