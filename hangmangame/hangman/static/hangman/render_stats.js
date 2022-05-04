$(document).on("click", "#id-statistics-button", function() {
    var url = $(this).attr("stats-url");
  
    $.ajax({
      url: url,
      success: function (data) {
        $("#id-stats-fields").html(data);
        document.getElementById("id-stats-fields").style.display = "block";
      }
    });
});

$(document).click(function(e) {
    if (e.target.id != 'id-stats-fields' && !$('#id-stats-fields').find(e.target).length)
    {
        $("#id-stats-fields").hide();
    }
});