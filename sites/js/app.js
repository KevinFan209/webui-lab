// 首頁：查詢伺服器即時狀態、處理白名單申請表單
const statusWidget = document.getElementById("statusWidget");
const whitelistForm = document.getElementById("whitelistForm");
const formMessage = document.getElementById("formMessage");

function renderStatus(data) {
    if (!data.online) {
        statusWidget.innerHTML = `
            <span class="status-dot is-offline"></span>
            <span class="state-message">伺服器目前離線</span>
        `;
        return;
    }

    statusWidget.innerHTML = `
        <span class="status-dot is-online"></span>
        <span class="state-message">
            在線中 · ${data.players_online}/${data.players_max} 人 · ${data.version}
        </span>
    `;
}

function renderStatusError() {
    statusWidget.innerHTML = `<span class="state-message">狀態查詢失敗，請重新整理頁面。</span>`;
}

async function loadStatus() {
    try {
        const response = await fetch("api/status");
        const data = await response.json();
        renderStatus(data);
    } catch (error) {
        console.error("查詢伺服器狀態失敗", error);
        renderStatusError();
    }
}

async function submitWhitelistApplication(event) {
    event.preventDefault();

    const minecraftId = document.getElementById("minecraftId").value.trim();
    const note = document.getElementById("note").value.trim();

    formMessage.textContent = "送出中…";

    try {
        const response = await fetch("api/whitelist-apply", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ minecraft_id: minecraftId, note: note }),
        });
        const data = await response.json();

        if (response.ok) {
            formMessage.textContent = data.message;
            whitelistForm.reset();
        } else {
            formMessage.textContent = data.error || "送出失敗，請確認格式是否正確。";
        }
    } catch (error) {
        console.error("送出白名單申請失敗", error);
        formMessage.textContent = "送出失敗，請稍後再試一次。";
    }
}

whitelistForm.addEventListener("submit", submitWhitelistApplication);

loadStatus();
