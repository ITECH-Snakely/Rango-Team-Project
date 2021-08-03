$(document).ready(function() {
    $('#dislike_btn').click(function() {
        var catecategoryIdVar;
        catecategoryIdVar = $(this).attr('dislikeData-categoryid');

        $.get('/rango/dislike_category/',
              {'category_id': catecategoryIdVar},
              function(newData) {
                var jsonData = newData;
                $('#dislike_count').html(jsonData.dislikeData);
                $('#like_count').html(jsonData.likeData);
                $('#dislike_btn').hide();
              })         
    });
});