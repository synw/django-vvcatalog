{% load i18n vvcatalog_tags %}
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
			img = app.getImgUrl(cat.image);
			cat.image = img;
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
			cat.image = app.getImgUrl(cat.image);
			cats.push(cat);
			i++
		}
  		app.categories = cats;
  		app.activate(["categories"]);
	}
	runQuery(q, action, error);
	return
},
getProducts: function(slug) {
	var after = "";
	if (this.endCursor !== undefined) {
		after = ', after:"'+this.endCursor+'"'
	}
	var q = 'query{category(slug:"'+slug+'"){slug,title,products(';
	q = q+'first:{% get_pagination %}'+after+'){edges{node{slug,title,navimage,price}cursor}';
	q=q+'pageInfo{startCursor,endCursor,hasNextPage,hasPreviousPage}}}}';
	function error(err) {
		console.log("An error has occured", err);
	}
	function action(data) {
		var products = [];
		var prods = data.category.products.edges;
		app.flush('products');
		app.currentCategory = data.category.slug;
		i=0;
		while (i<prods.length) {
			var prod = prods[i].node;
			prod.navimage = app.getProductImgUrl(prod.navimage);
			app.products.push(prod);
			i++
		}
		if ( app.currentProductXsIndex === 0 ) { 
			app.currentProductXs = prods[0].node;
		}
		//console.log("CURRENT XS", app.str(app.currentProductXs));
  		app.activate(["products"]);
		app.hasNextPage = data.category.products.pageInfo.hasNextPage;
		if (app.hasNextPage === true) {
			app.endCursor = data.category.products.pageInfo.endCursor;
		} else {
			app.endCursor = undefined
		}
	}
	runQuery(q, action, error);
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
next: function() {
	var total = this.products.length;
	var index = total-1;
	if (this.currentProductXsIndex === (index-1)) {
		if (this.hasNextPage === true) {
			//console.log((this.currentProductXsIndex)+" / "+(index));
			this.getProducts(this.currentCategory);
		}
	}
	if (this.currentProductXsIndex === index) {
		if (this.hasNextPage !== true) {
			this.currentProductXsIndex = 0;
		} else {
			this.currentProductXsIndex++;
		}
	} else if (this.currentProductXsIndex < index) {
		this.currentProductXsIndex++
	}
	this.currentProductXs = this.products[this.currentProductXsIndex]
},
prev: function() {
	var total = this.products.length;
	var index = total-1;
	if (this.currentProductXsIndex > 0){
		this.currentProductXsIndex--
	} else if (this.currentProductXsIndex == 0){
		this.currentProductXsIndex = index
	}
	this.currentProductXs = this.products[this.currentProductXsIndex]
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
getScreenWidth() {
	var width = window.innerWidth
	|| document.documentElement.clientWidth
	|| document.body.clientWidth;
	return width
},
getImgUrl(img) {
	img = img.replace("uploads/", "");
	img = "/media/_versions/"+img;
	var width = this.getScreenWidth();
	if (width < 350) {
		img = img.replace(".jpg", "_thumbnail.jpg");
	} else if (width > 350 && width < 768) {
		img = img.replace(".jpg", "_small.jpg");
	} else if (width >= 768 && width < 1024) {
		img = img.replace(".jpg", "_medium.jpg");
	} else {
		img = img.replace(".jpg", "_big.jpg");
	}
	return img
},
getProductImgUrl(img) {
	img = img.replace("uploads/", "");
	img = "/media/_versions/"+img;
	var width = this.getScreenWidth();
	if (width < 769) {
		img = img.replace(".jpg", "_medium.jpg");
	} else {
		img = img.replace(".jpg", "_big.jpg");
	}
	return img
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
