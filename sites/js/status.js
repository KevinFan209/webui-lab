document.addEventListener("DOMContentLoaded", function () {
    const serverStatus = document.getElementById("server-status");
    const whitelistForm = document.getElementById("whitelist-form");

    fetch("/api/status")
        .then(function (response) {
            return response.json();
        })
        .then(function (data) {
            if (data.online) {
                serverStatus.textContent =
                    `伺服器在線：${data.players_online} / ${data.players_max} 位玩家`;
            } else {
                serverStatus.textContent = "伺服器離線";
            }
        });

    whitelistForm.addEventListener("submit", async function (event) {
        event.preventDefault();

        const formData = new FormData(whitelistForm);
        const minecraftId = formData.get("minecraft_id");
        const note = formData.get("note");

        try {
            const response = await fetch("/api/whitelist-apply", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json"
                },
                body: JSON.stringify({
                    minecraft_id: minecraftId,
                    note: note
                })
            });
            const data = await response.json();

            if (response.ok) {
                alert(data.message);
                whitelistForm.reset();
            } else {
                alert(data.error);
            }
        } catch (error) {
            alert("申請失敗，請稍後再試");
        }
    });
});
