$(document).on('click', '.btn-primary', function(e) {
    var l = $(this).attr('id');
    $.ajax({
        type: 'GET',
        url: $(this).attr('update-letters-url'),
        data: {
            'letter': l
        },
        success: function(data) {
            console.log(data.finished);
            if (data.finished) {
                $(".main").html("YOU SAVED THE MAN!");
            } else {
                window.location.reload();
            }
            
            // $("#" + l).hide();
            // console.log(data);
            
            // $("#id-word-status").html(data.current_status);

            // if (data.classification === false) {
            //     $("#id-used-letters").append("<button class='btn btn-danger'>" + l.toUpperCase() + "</button>");
            // } else {
            //     $("#id-used-letters").append("<button class='btn btn-success'>" + l.toUpperCase() + "</button>");
            // }
        }
    });
});