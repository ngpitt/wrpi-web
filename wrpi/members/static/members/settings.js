function settings(form) {
    $.post(".", $(form).serialize(), function(json) {
        if (json.login) {
            $("#message").html("Saved.");
        } else {
            $("#message").html("Invalid fields.");
        }
    }, "json");
}
