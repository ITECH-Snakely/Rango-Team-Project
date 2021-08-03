$(document).ready(function() {
    $('#like_btn').click(function() {
        var catecategoryIdVar;
        catecategoryIdVar = $(this).attr('likeData-categoryid');

        $.get('/rango/like_category/',
              {'category_id': catecategoryIdVar},
              function(newData) {
                  const jsonParser = JSON.parse(newData);
                  $('#like_count').html(jsonParser.likeData);
                  $('#dislike_count').html(jsonParser.dislikeData);
                  $('#like_btn').hide();
              })
    });
});

