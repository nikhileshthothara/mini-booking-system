document.addEventListener("DOMContentLoaded", function () {
    const form = document.getElementById("signup-form");

    form.addEventListener("submit", function (event) {
        event.preventDefault();

        const formData = new FormData(form);
        const csrfToken = document.querySelector("[name=csrfmiddlewaretoken]").value;

        fetch(form.action, {
            method: "POST",
            body: formData,
            headers: {
                "X-CSRFToken": csrfToken
            }
        })
        .then(response => response.json())
        .then(data => {
            document.querySelectorAll(".errors").forEach(div => div.innerHTML = "");

            if (data.success) {
                window.location.href = data.redirect_url;
            } else {
                for (const field in data.errors) {
                    const errorDiv = document.getElementById("error_" + field);
                    data.errors[field].forEach(error => {
                        const p = document.createElement("p");
                        p.textContent = error;
                        errorDiv.appendChild(p);
                    });
                }
            }
        })
        .catch(error => console.error("Error:", error));
    });
});
