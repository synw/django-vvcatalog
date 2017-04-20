var slider = document.getElementById('product-xs');
var mc = new Hammer(slider);
mc.on("swipeleft", function(ev) {
    app.next();
});
mc.on("swiperight", function(ev) {
	app.prev();
});
document.onkeydown = function(evt) {
    evt = evt || window.event;
    switch (evt.keyCode) {
        case 37:
        	app.prev();
            break;
        case 39:
        	app.next();
            break;
    }
};
function post_order() {
	url = "{% url 'create-order' %}";
	var data = {};
	data["cart"] = app.cart;
	$.ajax({
	      type: 'POST',
	      contentType: "application/json; charset=utf-8",
	      url: url,
	      data: JSON.stringify(data),
	      success: function (response) {
	    	  app.flush();
    		  app.activate("postedOrder");
	    	  if (response.ok === 1) {
	    		  app.cart = [];
	    		  store.set("cart", []);
	    		  self.location.href = "#top";
	    		  page("/catalog/order/ok/");
	    	  } else {
	    		  self.location.href = "#top";
	    		  page("/catalog/order/error/");
	    	  }
	      },
	      error: function(xhr, textStatus, error) {
	      	console.log("Error:");
	          console.log(xhr.statusText);
			    console.log(textStatus);
			    console.log(error);
	      }
	  })
}
{% include "graphql_utils/methods.js" %}
var stored_cart = store.get("cart") || [];
if (stored_cart.length > 0) {
	app.cart = stored_cart;
	app.ShowToggleBtn();
}