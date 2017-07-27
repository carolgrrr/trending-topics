jQuery(document).ready(function(){
	jQuery( "#submit" ).click(function() {
  		//alert( "Handler for .click() called." );

  		var boxes = jQuery(":checkbox:checked");
  		var hashtags = [];

  		jQuery("input:checked").each(function() {
  			var id = this.id;
  			alert(id);
  			hashtags.push(id);
  		});
	});
});
