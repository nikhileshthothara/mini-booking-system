document.addEventListener("DOMContentLoaded", function () {
    const form = document.getElementById("bookings-form");

    form.addEventListener("submit", function (event) {
        event.preventDefault();
        const alertDiv = document.querySelector(".alert-danger");
        alertDiv.style.display = "none";
        alertDiv.textContent = "";
        
        const formData = new FormData(form);
        const csrfToken = document.querySelector("[name=csrfmiddlewaretoken]").value;
        const bookingId = form.dataset.bookingId;
        const actionUrl = `/bookings/${bookingId}/update/`;

        fetch(actionUrl, {
            method: "POST",
            body: formData,
            headers: {
                "X-CSRFToken": csrfToken
            }
        })
        .then(response => response.json())
        .then(data => {
            document.querySelectorAll(".text-danger").forEach(div => div.innerHTML = "");

            if (data.success) {
                window.location.href = data.redirect_url;
            } else {
                if (data.errors) {
                    alertDiv.style.display = "block";
                    alertDiv.textContent = data.errors['__all__'];
                }
                for (const field in data.errors) {
                    const errorDiv = document.getElementById("error_" + field);
                    if (errorDiv) {
                        data.errors[field].forEach(error => {
                            const p = document.createElement("p");
                            p.textContent = error;
                            errorDiv.appendChild(p);
                        });
                    }
                }
            }
        })
        .catch(error => console.error("Error:", error));
    });
});
