function auth(form) {
    $.post(".", $(form).serialize(), function(json) {
        if (json.login) {
            $("#content").load("home");
        } else {
            $("#message").html("Invalid credentials.");
        }
    }, "json");
}
