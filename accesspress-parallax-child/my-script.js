alert("my script has loaded.");

(function( $ )) {
  $(document).ready(function(){

    $( "#submit" ).click(function() {
      //alert( "Handler for .click() called." );

      var boxes = jQuery(":checkbox:checked");
      var hashtags = [];

      $("input:checked").each(function() {
        var id = this.id;
        alert(id);
        hashtags.push(id);
      });
    });
  });
})( jQuery );


