$(document).ready(function() {
    $("#id-profile-button").click(function(e) {
        e.preventDefault();
        
        $.ajax({
            type: 'GET',
            url: $(this).attr("href"),
            success: function(response) {
                $("#id-profile-fields").html(response);
                document.getElementById("id-profile-fields").style.display = "block";
            },
            error: function(response) {

            }
        });
    });

    $(document).click(function(e) {
        if (e.target.id != 'id-profile-fields' && !$('#id-profile-fields').find(e.target).length)
        {
            $("#id-profile-fields").hide();
        }
    });
});

$(document).on('click', '#id-profile-update-button', function(e) {
    e.preventDefault();
    
    $.ajax({
        type: 'GET',
        url: $(this).attr("href"),
        success: function(response) {
            $("#id-profile-fields").html(response);
        }
    });
});

$(document).on('click', '#id-profile-update-cancel', function(e) {
    e.preventDefault();
    
    $.ajax({
        type: 'GET',
        url: $("#id-profile-button").attr("href"),
        success: function(response) {
            $("#id-profile-fields").html(response);
        }
    });
});

$(document).on('submit', '#id-profile-update-form', function(e) {
    e.preventDefault();
    var formData = new FormData();

    $.each($(this).serializeArray(), function(index, value) {
        formData.append(value['name'], value['value']);
    });

    var img_data = $('#id_image').get(0).files[0];
    if (img_data) {
        formData.append('image', img_data);
    }
    
    $.ajax({
        type: 'POST',
        url: $(this).attr("action"),
        data: formData,
        contentType: false,
        cache: false,
        processData: false,
        enctype: 'multipart/form-data',
        success: function(response1) {
            $.ajax({
                type: 'GET',
                url: $("#id-profile-button").attr("href"),
                success: function(response2) {
                    $("#id-profile-fields").html(response2);
                }
            });
        }
    });
});