$(document).ready(function() {
    $('#dislike_btn').click(function() {
        var catecategoryIdVar;
        catecategoryIdVar = $(this).attr('dislikeData-categoryid');

        $.get('/rango/dislike_category/',
              {'category_id': catecategoryIdVar},
              function(newData) {
                const jsonParser = JSON.parse(newData);
                $('#dislike_count').html(jsonParser.dislikeData);
                $('#like_count').html(jsonParser.likeData);
                $('#dislike_btn').hide();
              })         
    });
});