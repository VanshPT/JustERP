var user_list = document.getElementById("user-list");
var create_user = document.getElementById("create-user");
var permission = document.getElementById("permission");
var profiles = document.getElementById("profiles");
var logs = document.getElementById("logs");

var elements = [user_list, create_user, permission, profiles, logs];

elements.forEach(function(element) {
    element.addEventListener("click", function() {
        elements.forEach(function(el) {
            el.classList.remove('active');
        });

        this.classList.add('active');
    });
});
