const username = sessionStorage.getItem("username");

async function loadMessages() {
    const response = await fetch("/api/chat");
    const messages = await response.json();
    const chatMessages = document.getElementById("chat-messages");

    chatMessages.innerHTML = "";
    messages.forEach(function (message) {
        const messageElement = document.createElement("div");
        messageElement.textContent = `${message.username}: ${message.message}`;
        chatMessages.append(messageElement);
    });
}

document.addEventListener("DOMContentLoaded", function () {
    loadMessages();
    setInterval(loadMessages, 3000);

    const chatForm = document.getElementById("chat-form");
    chatForm.addEventListener("submit", async function (event) {
        event.preventDefault();

        const formData = new FormData(chatForm);
        const message = formData.get("message");
        if (message === "") {
            return;
        }

        try {
            const response = await fetch("/api/chat", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json"
                },
                body: JSON.stringify({ username, message })
            });
            const data = await response.json();

            if (response.ok) {
                chatForm.elements.message.value = "";
                loadMessages();
            } else {
                alert(data.error);
            }
        } catch (error) {
            alert("訊息送出失敗，請稍後再試");
        }
    });
});
