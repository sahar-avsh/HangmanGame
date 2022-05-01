$(document).on('change', '#id-word_source_field', function() {
    if ($(this).val() === 'U') {
        document.getElementById("id-guess-word").style.display = "block";
        document.getElementById("id-word-difficulty").style.display = "none";
        $("#id-guess_word-field").attr('required', true);
    } else {
        document.getElementById("id-word-difficulty").style.display = "block";
        document.getElementById("id-guess-word").style.display = "none";
        $("#id-guess_word-field").attr('required', false);
    }
});