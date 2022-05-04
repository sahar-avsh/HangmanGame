function get_countdown_status(time_remaining) {
    var hours = Math.floor((time_remaining % (1000 * 60 * 60 * 24)) / (1000 * 60 * 60));
    var minutes = Math.floor((time_remaining % (1000 * 60 * 60)) / (1000 * 60));
    var seconds = Math.floor((time_remaining % (1000 * 60)) / 1000);

    return hours + ":" + minutes + ":" + seconds;
}

$(document).ready(function() {
    var active_games = $("#id-games").attr("data-id");
    // console.log(active_games);

    active_games = active_games.replace(/ /g, "").replace(/\[/g, "").replace(/\]/g, "");
    // console.log(active_games);

    ids = active_games.split(",");
    // console.log(ids);

    for (i = 0; i < ids.length; i++) {
        // console.log(ids[i]);
        // console.log(localStorage.getItem("duration#" + ids[i]));
        if (localStorage.getItem("duration#" + ids[i])) {
            $("#id-time-" + ids[i]).replaceWith(get_countdown_status(localStorage.getItem("duration#" + ids[i])));
        }
    }
});



