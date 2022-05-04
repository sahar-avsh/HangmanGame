function get_countdown_status(time_remaining) {
    var hours = Math.floor((time_remaining % (1000 * 60 * 60 * 24)) / (1000 * 60 * 60));
    var minutes = Math.floor((time_remaining % (1000 * 60 * 60)) / (1000 * 60));
    var seconds = Math.floor((time_remaining % (1000 * 60)) / 1000);

    return hours + ":" + minutes + ":" + seconds;
}

function timeToMilliSeconds(time) {
    time = time.split(/:/);
    milliseconds = (time[0] * 3600 + time[1] * 60 + parseInt(time[2])) * 1000
    return milliseconds;
}

function getStorage() {
    var dict = {}
    keys = Object.keys(localStorage);
    i = keys.length;

    while (i--) {
        dict[keys[i].split('#')[1]] = localStorage.getItem(keys[i]);
        $("#id-time-" + keys[i].split('#')[1]).replaceWith(get_countdown_status(localStorage.getItem(keys[i])));
    }
    return dict
}

$(document).ready(function() {
    var active_games = $("#id-games").attr("data-id");
    // console.log(active_games);

    if (active_games) {
        //active_games = active_games.replace(/ /g, "").replace(/\[/g, "").replace(/\]/g, "");
        // console.log(active_games);
    
        //ids = active_games.split(",");
        // console.log(ids);
    
        var csrftoken = $("[name=csrfmiddlewaretoken]").val();
        // console.log(getStorage());

        // TODO: send PUT ajax request and send all ids and durations in one request
        // unpack in server side and update all game states
        // return and write the response
        // hide spinner and show games

        // var ids = allStorageKeys();
        // var durations = allStorageValues();
        // var data = {
        //     'ids': ids,
        //     'time_remaining_list': durations
        // };

        var post_data = getStorage();

        $.ajax({
            type: 'POST',
            headers: {'X-CSRFToken': csrftoken},
            url: $("#id-games").attr("update-time-remaining-url"),
            data: post_data,
            success: function(data) {
                $(".spinner").hide();
                $("#id-games").show();
                localStorage.clear();
            },
            error: function(data) {
                $(".spinner").replaceWith("<div class='alert alert-primary' style='text-align: center;'>Error while loading games, please refresh!</div>");
            }
        });
    
        // for (i = 0; i < ids.length; i++) {
        //     // console.log(ids[i]);
        //     // console.log(localStorage.getItem("duration#" + ids[i]));
        //     var dur_ls = localStorage.getItem("duration#" + ids[i]);
        //     var dur_db = $("#id-time-remaining-" + ids[i]).attr("data-id");
        //     if (dur_ls !== null && dur_db != dur_ls) {
        //         $.ajax({
        //             type: 'POST',
        //             headers: {'X-CSRFToken': csrftoken},
        //             url: $("#id-games").attr("update-time-remaining-url"),
        //             data: {
        //                 'id': ids[i],
        //                 'time_remaining' : dur_ls
        //             },
        //             success: function(data) {
        //                 localStorage.removeItem("duration#" + ids[i]);
        //             }
        //         });
        //     }
    
        //     // if (dur_ls) {
        //     //     $("#id-time-" + ids[i]).replaceWith(get_countdown_status(dur_ls));
        //     // }
        // }
    }


    // setTimeout(() => {
    //     $.ajax({
    //         type: 'GET',
    //         url: window.location.href,
    //         success: function(data) {
    //             if (data.ids) {
    //                 for (j = 0; j < data.ids.length; j++) {
    //                     $("#id-time-" + String(data.ids[j])).replaceWith(get_countdown_status(parseInt(data.durations[j])));
    //                 }
    //                 $(".spinner").hide();
    //                 $("#id-games").show();
    //             }
    //         },
    //         error: function(data) {
    //             $(".spinner").replaceWith("<div class='alert alert-primary' style='text-align: center;'>Error while loading games, please refresh!</div>");
    //         }
    //     });
    // }, 500);

});



