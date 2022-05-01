$(document).ready(function(){

  $("#id-login-button").click(function () {
      var url = $("#id-login-button").attr("login-form-url");
  
      $.ajax({
        url: url,
        success: function (data) {
          $("#id-login-form-fields").html(data);
          document.getElementById("id-login-form-fields").style.display = "block";
        }
      });
    });

  $("#id-register-button").click(function () {
    var url = $("#id-register-button").attr("register-form-url");

    $.ajax({
      url: url,
      success: function (data) {
        $("#id-register-form-fields").html(data);
        document.getElementById("id-register-form-fields").style.display = "block";
      }
    });
  });

  $("#id-start-game-button").click(function () {
    var url = $("#id-start-game-button").attr("start-game-form-url");

    $.ajax({
      url: url,
      success: function (data) {
        $("#id-start-game-form-fields").html(data);
        document.getElementById("id-start-game-form-fields").style.display = "block";
      }
    });
  });
})

$(document).click(function(e) {
  if (e.target.id != 'id-login-form-fields' && !$('#id-login-form-fields').find(e.target).length)
  {
      $("#id-login-form-fields").hide();
  }

  if (e.target.id != 'id-register-form-fields' && !$('#id-register-form-fields').find(e.target).length)
  {
      $("#id-register-form-fields").hide();
  }

  if (e.target.id != 'id-start-game-form-fields' && !$('#id-start-game-form-fields').find(e.target).length)
  {
      $("#id-start-game-form-fields").hide();
  }
});


$(document).on('submit', '#id-login-form', function(e) {
  e.preventDefault();

  $.ajax({
    type: "POST",
    url: this.action,
    data: $(this).serialize(),
    success: function(data) {
      //$('body').replaceWith(data);
      window.location.reload();
    },
    error: function(data) {
      var div_error = document.createElement("div");
      $(div_error).css('margin-bottom', '0px');
      $(div_error).text(data.responseJSON.status);
      div_error.classList.add("alert");
      div_error.classList.add("alert-dark");
      $('.container-form').append(div_error);
    }
  });
});

$(document).on('submit', '#id-register-form', function(e) {
  e.preventDefault();

  $.ajax({
    type: "POST",
    url: this.action,
    data: $(this).serialize(),
    success: function(data) {
      //$('body').replaceWith(data);
      window.location.reload();
    },
    error: function(data) {
      $.each(data.responseJSON.status, function(index, value) {
        $("#id-error-div-" + index).remove();
        var div_error_signup = document.createElement("div");
        $(div_error_signup).attr('id', 'id-error-div-' + index);
        $(div_error_signup).css('margin-bottom', '0px');

        $.each(value, function(i) {
          var p = document.createElement("p");
          $(p).css('margin-bottom', '0px');
          p.append(value[i]);
          $(div_error_signup).append(p);
        })

        div_error_signup.classList.add("alert");
        div_error_signup.classList.add("alert-dark");
        $("#div_id_" + index).append(div_error_signup);
      });
    }
  });
});

// $(document).on('submit', '#id-start-game-form', function(e) {
//   e.preventDefault();

//   $.ajax({
//     type: "POST",
//     url: this.action,
//     data: $(this).serialize(),
//     success: function(data) {
//     },
//     error: function(data) {
//     }
//   });
// });