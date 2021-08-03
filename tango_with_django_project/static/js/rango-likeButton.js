$(document).ready(function() {
    $('#like_btn').click(function() {
        var catecategoryIdVar;
        catecategoryIdVar = $(this).attr('likeData-categoryid');

        $.get('/rango/like_category/',
              {'category_id': catecategoryIdVar},
              function(newData) {
                  var jsonData = newData;
                  $('#like_count').html(jsonData.likeData);
                  $('#dislike_count').html(jsonData.dislikeData);
                  $('#like_btn').hide();
              })
    });
});

