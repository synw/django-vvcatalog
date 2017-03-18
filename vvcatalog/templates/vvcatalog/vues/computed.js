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
		if (this.delivery === true) {
			return "block"
		}
		return "none"
	},
	set: function (newValue) {
		if (this.delivery === true) {
			return "block"
		}
		return "none"
	}
},
showFinalOrder: {
	get: function () {
		if (this.deliveryAccepted === false) {
			return "none"
		}
		return "block"
	},
	set: function () {
		if (this.deliveryAccepted === false) {
			return "none"
		}
		return "block"
	}
},
sumNotOk: {
	get: function () {
		if (this.sumAccepted == false) {
			return "block"
		}
		return "none"
	},
	set: function (newValue) {
		if (this.sumAccepted == false) {
			return "block"
		}
		return "none"
	}
},
sumOk: {
	get: function () {
		if (this.sumAccepted == true) {
			return "block"
		}
		return "none"
	},
	set: function (newValue) {
		if (this.sumAccepted == true) {
			return "block"
		}
		return "none"
	}
},
