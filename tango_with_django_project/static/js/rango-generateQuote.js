$(document).ready(function() {
    $('#quote_generator').click(function() {

        $.get('/rango/generate_quote/',
              function(newQuote){
                $('#quote_display').html(newQuote);

              })
    });
});