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