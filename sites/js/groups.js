const groupListUsername = sessionStorage.getItem("username");

async function loadGroups() {
    const response = await fetch(
        `/api/groups?username=${encodeURIComponent(groupListUsername)}`
    );
    const groups = await response.json();
    const groupsList = document.getElementById("groups-list");

    groupsList.innerHTML = "";
    groups.forEach(function (group) {
        const groupItem = document.createElement("li");
        groupItem.textContent = group.name;
        groupsList.append(groupItem);
    });
}

document.addEventListener("DOMContentLoaded", function () {
    loadGroups();

    const createGroupForm = document.getElementById("create-group-form");
    createGroupForm.addEventListener("submit", async function (event) {
        event.preventDefault();

        const formData = new FormData(createGroupForm);
        const groupName = formData.get("group_name");

        try {
            const response = await fetch("/api/groups/create", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json"
                },
                body: JSON.stringify({
                    username: groupListUsername,
                    name: groupName
                })
            });
            const data = await response.json();

            if (response.ok) {
                createGroupForm.elements.group_name.value = "";
                loadGroups();
            } else {
                alert(data.error);
            }
        } catch (error) {
            alert("建立群組失敗，請稍後再試");
        }
    });

    const joinGroupForm = document.getElementById("join-group-form");
    joinGroupForm.addEventListener("submit", async function (event) {
        event.preventDefault();

        const formData = new FormData(joinGroupForm);
        const groupName = formData.get("group_name");

        try {
            const response = await fetch("/api/groups/join", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json"
                },
                body: JSON.stringify({
                    username: groupListUsername,
                    group_name: groupName
                })
            });
            const data = await response.json();

            if (response.ok) {
                alert(`已成功加入群組${groupName}`);
                joinGroupForm.elements.group_name.value = "";
                loadGroups();
            } else {
                alert(data.error);
            }
        } catch (error) {
            alert("加入群組失敗，請稍後再試");
        }
    });
});
