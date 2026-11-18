document.addEventListener("DOMContentLoaded", function () {
    const loginForm = document.querySelector(".login-form");
    const registerForm = document.querySelector(".register-form");

    loginForm.addEventListener("submit", async function (event) {
        event.preventDefault();

        const formData = new FormData(loginForm);
        const username = formData.get("username");
        const password = formData.get("password");

        try {
            const response = await fetch("/api/login", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json"
                },
                body: JSON.stringify({ username, password })
            });
            const data = await response.json();

            if (response.ok) {
                alert("登入成功");
                window.location.href = "homepage.html";
            } else {
                alert(data.error);
            }
        } catch (error) {
            alert("登入失敗，請稍後再試");
        }
    });

    registerForm.addEventListener("submit", async function (event) {
        event.preventDefault();

        const formData = new FormData(registerForm);
        const username = formData.get("new_username");
        const email = formData.get("new_email");
        const password = formData.get("new_password");

        try {
            const response = await fetch("/api/register", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json"
                },
                body: JSON.stringify({ username, email, password })
            });
            const data = await response.json();

            if (response.ok) {
                alert("註冊成功");
                registerForm.reset();
            } else {
                alert(data.error);
            }
        } catch (error) {
            alert("註冊失敗，請稍後再試");
        }
    });
});
