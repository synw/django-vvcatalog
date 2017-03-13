{% load i18n %}

Vue.component('categories', {
    template: '#categories-template',
    props:['list']
    });

Vue.component('products', {
    template: '#products-template',
    props:['list']
    });

Vue.component('cart', {
    template: '#cart-template',
    props:['list']
    });

const app = new Vue({
	el: '#app',
	data: {
		title: "",
		content: "",
		header: '',
		header_ori: "display:block",
		footer: '',
		footer_ori: "display:block",
		vtitle: "title",
	    categories: [],
	    products:[],
	    noCats:"hidden",
	    current_category: "",
	    cart:[],
	    cartTotal:-1,
	},
	methods: {
		createCartItem: function(product) {
			var cart_item = {"product":product, "num":1, "price":product.price, "slug":product.slug};
			return cart_item
		},
		getCartItem: function(product) {
        	for (i=0;i<this.cart.length;i++) {
        		if (this.cart[i].product == product) {
        			return this.cart[i]
        		}
        	}
        	return null
        },
        AddToCart: function(product) {
        	var cart_item = this.getCartItem(product);
        	if (cart_item != null) {;
        		cart_item.num = cart_item.num+1;
        		cart_item.price = cart_item.price+product.price;
        	} else {
        		var cart_item = this.createCartItem(product);
        		this.cart.push(cart_item);
        	}
        },
        RemoveFromCart: function(cart_item) {
        	if (cart_item.num < 2) {
        		this.cart.pop(cart_item);
        	} else {
        		cart_item.num = cart_item.num-1;
        		cart_item.price = cart_item.price-cart_item.product.price;
        	}
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
        SwapHeader: function(header) {
        	if (header == "ori") {
        		this.header_ori = "display:block";
        		this.header = "";
        	}
        },
        SwapFooter: function(footer) {
        	if (footer == "ori") {
        		this.footer_ori = "display:block";
        		this.footer = "";
        	}
        }
	},
	computed: {
		Total: function () {
		t = 0;
		for (i=0;i<this.cart.length;i++) {
			price = this.cart[i].price;
			t = t+price
		}
		this.cartTotal = t;
		return t
		}
	},
})
 
function listCats(resturl, current_category) {
	promise.get(resturl,{},{"Accept":"application/json"}).then(function(error, data, xhr) {
	    if (error) {console.log('Error ' + xhr.status);return;}    
	    data = JSON.parse(data);
	    // check content type
	    app.SwapHeader("ori");
	    if (data.length > 0) {
	    	app.noCats = "hidden";
		    content_type = data[0].content_type;
		    if (content_type == "product") {
		    	app.categories = [];
		    	app.products = data;
		    } else {
		    	app.products = [];
		    	app.categories = data;
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
}

function printProd(resturl) {
	promise.get(resturl,{},{"Accept":"application/json"}).then(function(error, data, xhr) {
	    if (error) {console.log('Error ' + xhr.status);return;}
	    data = JSON.parse(data);
	    app.products = data;
	    top.document.title = "{% trans 'Products' %}";
	});
	return
}

function HandleOrder() {
	var resturl = "{% url 'is-authenticated' %}";
	promise.get(resturl,{}, {"Accept":"application/json"}).then(function(error, data, xhr) {
	    if (error) {console.log('Error ' + xhr.status);return;}
	    data = JSON.parse(data);
	    if (data.is_authenticated == true) {
	    	console.log("logged_in")
	    } else {
	    	document.getElementById('login').style.display="block";
	    	document.getElementById('order').style.display="none";
	    }
	});
}

function goAuth(from) {
	var resturl = "{% url 'set-cart' %}";
	resturl = resturl+"?"+encodeCartData();
	resturl = resturl+"from="+from;
	self.location.href = resturl;
}

function gotoContent() {
	self.location.href="#top";
}

function encodeCartData() {
	var str = "";
	for (i=0;i<app.cart.length;i++) {
		var item = app.cart[i];
		str = str+item.slug+"="+item.num+"&";
	}
	return str
}
 