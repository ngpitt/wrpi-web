function auth(form) {
    $.post(".", $(form).serialize(), function(json) {
        if (json.login) {
            window.location = "home";
        } else {
            $("#message").html("Invalid credentials.");
        }
    }, "json");
}
