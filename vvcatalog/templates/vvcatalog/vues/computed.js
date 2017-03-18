Total: function () {
	t = 0;
	for (i=0;i<this.cart.length;i++) {
		price = this.cart[i].price;
		t = t+price
	}
	if (t == 0) {
		var cart = document.getElementById('cart');
		if (cart != null) {
			this.HideCart();
		}
	}
	store.remove("total");
	store.set("total", t);
	return t
},
showCustomerForm: {
	get: function () {
		if (this.active.indexOf("customer_form") > -1) {
			return "block"
		}
		return "none"
	},
	set: function (newValue) {
		if (this.active.indexOf("customer_form") > -1) {
			return "block"
		}
		return "none"
	}
},
showSummary: {
	get: function () {
		if (this.active.indexOf("summary") > -1) {
			return "block"
		}
		return "none"
	},
	set: function (newValue) {
		if (this.active.indexOf("summary") > -1) {
			return "block"
		}
		return "none"
	}
},
showDelivery: {
	get: function () {
		if (this.active.indexOf("delivery") > -1) {
			return "block"
		}
		return "none"
	},
	set: function (newValue) {
		if (this.active.indexOf("delivery") > -1) {
			return "block"
		}
		return "none"
	}
},
showFinalOrder: {
	get: function () {
		if (this.active.indexOf("final_order") > -1) {
			return "block"
		}
		return "none"
	},
	set: function (newValue) {
		if (this.active.indexOf("final_order") > -1) {
			return "block"
		}
		return "none"
	}
},