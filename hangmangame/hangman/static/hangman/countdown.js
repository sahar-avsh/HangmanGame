function timeToMilliSeconds(time) {
    time = time.split(/:/);
    milliseconds = (time[0] * 3600 + time[1] * 60 + parseInt(time[2])) * 1000
    return milliseconds;
}

function get_countdown_status(time_remaining) {
    var hours = Math.floor((time_remaining % (1000 * 60 * 60 * 24)) / (1000 * 60 * 60));
    var minutes = Math.floor((time_remaining % (1000 * 60 * 60)) / (1000 * 60));
    var seconds = Math.floor((time_remaining % (1000 * 60)) / 1000);

    return hours + ":" + minutes + ":" + seconds;
}

//var canCount = true;
//localStorage.setItem("canCount", canCount);

var time_allowed = $("#id-timer").attr("data-time-allowed");
if (typeof time_allowed !== "undefined") {
    var initial_value = timeToMilliSeconds(time_allowed); 
}


$(document).ready(function() {
    if (time_allowed !== "None") {
        var canCount = true
        $("#id-clock").html(canCount?"Pause Clock":"Continue Clock");

        var x;
        var duration = localStorage.getItem("duration");

        if (!duration) {
            duration = initial_value;
            localStorage.setItem("duration", initial_value);
        }

        $("#countdown").html(get_countdown_status(duration));

        // function startTimer() {
        if (localStorage.getItem("duration")) {
            // Update the count down every 1 second
            x = setInterval(function() {
                if (canCount) {
                    duration = duration - 1000;
                    localStorage.setItem("duration", duration);
                    // Display the result in the element with id="countdown"
                    $("#countdown").html(get_countdown_status(duration));
            
                    // If the count down is finished, write some text
                    if (duration < 0) {
                        clearInterval(x);
                        localStorage.removeItem("duration");
                        document.getElementById("countdown").innerHTML = "YOU HAVE LET THE MAN HANG!!!!!";
                    }
                }
            }, 1000);
        }
        // }

        // $("#id-start-timer").click(function() {
        //     startTimer();
        //     $(this).hide();
        //     localStorage.setItem("start-display", "none");
        // });

        $("#id-timer").click(function() {
            canCount = !canCount;
            $("#id-clock").html(canCount?"Pause Clock":"Continue Clock");
        });

        $("#id-reset-timer").click(function() {
            duration = initial_value;
            localStorage.setItem("duration", duration);
            $("#countdown").html(get_countdown_status(duration));
        });
    }
    // var start = localStorage.getItem("start-display");
    // if (start) {
    //     document.getElementById("id-start-timer").style.display = start;
    //     startTimer();
    // } else {
    //     document.getElementById("id-start-timer").style.display = "";
    // }
})




// var x;
// // var time_passed = 0;
// // localStorage.setItem("time_passed", time_passed);

// $(document).on('click', '#id-timer', function() {

//     if ($(this).text() === "Start Timer!") {
//         $(this).html("Stop Timer!");
//         $(this).removeClass("btn-info").addClass("btn-warning");

//         // $("#id-reset-timer").show();

//         var duration = localStorage.getItem("duration");
//         // time_passed = localStorage.getItem("time_passed");
//         if (!duration) {
//             var time_allowed = $("#id-timer").attr("data-time-allowed");
//             // duration = timeToMilliSeconds(time_allowed) - time_passed;
//             duration = timeToMilliSeconds(time_allowed);
//         }

//         // Update the count down every 1 second
//         x = setInterval(function() {

//             // Time calculations for days, hours, minutes and seconds
//             // var days = Math.floor(duration / (1000 * 60 * 60 * 24));
//             // var hours = Math.floor((duration % (1000 * 60 * 60 * 24)) / (1000 * 60 * 60));
//             // var minutes = Math.floor((duration % (1000 * 60 * 60)) / (1000 * 60));
//             // var seconds = Math.floor((duration % (1000 * 60)) / 1000);

//             // Display the result in the element with id="countdown"
//             // document.getElementById("countdown").innerHTML = days + "d " + hours + "h "
//             // + minutes + "m " + seconds + "s ";
//             $("#countdown").html(get_countdown_status(duration));

//             duration = duration - 1000;
//             localStorage.setItem("duration", duration);
//             // time_passed = time_passed + 1000;
//             // localStorage.setItem("time_passed", time_passed);

//             // If the count down is finished, write some text
//             if (duration < 0) {
//                 clearInterval(x);
//                 localStorage.removeItem("duration");
//                 document.getElementById("countdown").innerHTML = "YOU HAVE LET THE MAN HANG!!!!!";
//         }
//         }, 1000);
//     } else if ($(this).text() === "Stop Timer!") {
//         $(this).html("Start Timer!");
//         $(this).removeClass("btn-warning").addClass("btn-info");
//         clearInterval(x);
//     }
// })

// $(document).on('click', '#id-reset-timer', function() {
//     $("#id-timer").html("Start Timer!");
//     $("#id-timer").removeClass("btn-warning").addClass("btn-info");
//     // $(this).hide();
//     $("#countdown").html("");
//     localStorage.removeItem("duration");
//     clearInterval(x);
//     // time_passed = 0;
// })



// var initialValue = 50;
//    $(document).ready(function() {
//      var counter = localStorage.getItem("counter");
//      var canCount = true;
//      var id;
//      if (counter) {
//        $("span#count").html(counter);
//      } else {
//        localStorage.setItem("counter", initialValue);
//        counter = initialValue;
//        $("span#count").html(initialValue);
//      }

//      function startTimer() {
//        if (localStorage.getItem("counter") && id === undefined) {
//          id = setInterval(function() {
//            if (canCount) {
//              localStorage.setItem("counter", --counter);
//              span = document.getElementById("count");
//              span.innerHTML = counter;
//              if (counter <= 0) {
//                localStorage.removeItem("counter")
//                clearInterval(id);
//                id = undefined;
//              }
//            }
//          }, 1000);
//        }
//      }

//      $("#startClock").click(startTimer);

//      $("#restartClock").click(function(){
//         counter = initialValue;
//         localStorage.setItem("counter", counter);
//         $("span#count").html(counter);
//      });

//      $("#pauseClock").click(function() {
//        $(this).html(canCount?"Continue Clock":"Pause Clock");
//        canCount = !canCount;
//      });
//    });