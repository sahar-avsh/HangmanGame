$(document).ready(function() {
    // if (localStorage.getItem("image-number")) {
    //     num = localStorage.getItem("image-number");
    //     $("#id-hangman-status-1").hide();
    //     $("#id-hangman-status-" + num.toString()).show();
    // } else {
    //     localStorage.setItem("image-number", 1);
    // }
    var obj = {"6": "1", "5": "2", "4": "3", "3": "4", "2": "5", "1": "6", "0": "7"}
    var image_status = $("#id-guess-remaining").attr("remaining-guesses");
    $("#id-hangman-status-" + obj[image_status]).show();
})

$(document).on('click', '.btn-primary', function(e) {
    var l = $(this).attr('id');
    var id = $(this).attr('object-id');
    var csrftoken = $("[name=csrfmiddlewaretoken]").val();
    $.ajax({
        type: 'POST',
        headers: {'X-CSRFToken': csrftoken},
        url: $(this).attr('make-guess-url'),
        data: {
            'letter': l,
            'id': id
        },
        success: function(data) {
            if (data.is_game_finished) {
                // $(".main").html("YOU SAVED THE PERSON!");
                window.location.href = $("#id-game-over").attr("href");
                localStorage.removeItem("duration#" + String(id));
            }
            //     // localStorage.clear();
            // } else {
            // if (!data.is_game_finished) {
                // window.location.reload();
                document.getElementById(l).style.display = "none";
                $("#id-word-status").html(data.current_status.toUpperCase());
                
                for (t = 1; t < 8; t++) {
                    $("#id-hangman-status-" + t.toString()).hide();
                }
                
                $("#id-hangman-status-" + data.image).show();
                // localStorage.setItem("image-number", data.image);

                $("#id-ajax").html("");
                $("#id-used-letters-on-refresh").html("");
                for (i = 0; i < data.hits.length; i++) {
                    $("#id-ajax").append("<button class='btn btn-success' style='margin-right: 5px;'>" + data.hits[i].toUpperCase() + "</button>");
                }
                for (j = 0; j < data.misses.length; j++) {
                    $("#id-ajax").append("<button class='btn btn-danger' style='margin-right: 5px;'>" + data.misses[j].toUpperCase() + "</button>");
                }

                $("#id-guess-remaining").html("Guesses remaining: " + data.guesses_remaining);
            // }
            
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