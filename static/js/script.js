document.addEventListener("DOMContentLoaded", function () {
    document.querySelectorAll(".delete-form").forEach(function (form) {
        form.addEventListener("submit", function (event) {
            if (!confirm("Are you sure you want to delete this record?")) {
                event.preventDefault();
            }
        });
    });

    document.querySelectorAll(".alert").forEach(function (alert) {
        setTimeout(function () {
            var instance = bootstrap.Alert.getOrCreateInstance(alert);
            instance.close();
        }, 5000);
    });
}); 
