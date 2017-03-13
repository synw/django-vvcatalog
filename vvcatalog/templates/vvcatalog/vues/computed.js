Total: function () {
	t = 0;
	for (i=0;i<this.cart.length;i++) {
		price = this.cart[i].price;
		t = t+price
	}
	this.cartTotal = t;
	return t
}