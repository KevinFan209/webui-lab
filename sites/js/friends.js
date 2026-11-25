const currentUsername = sessionStorage.getItem("username");

async function loadFriends() {
    const response = await fetch(
        `/api/friends?username=${encodeURIComponent(currentUsername)}`
    );
    const friends = await response.json();
    const friendsList = document.getElementById("friends-list");

    friendsList.innerHTML = "";
    friends.forEach(function (friend) {
        const friendItem = document.createElement("li");
        friendItem.textContent = friend.username;
        friendsList.append(friendItem);
    });
}

document.addEventListener("DOMContentLoaded", function () {
    loadFriends();

    const addFriendForm = document.getElementById("add-friend-form");
    addFriendForm.addEventListener("submit", async function (event) {
        event.preventDefault();

        const formData = new FormData(addFriendForm);
        const friendUsername = formData.get("friend_username");

        try {
            const response = await fetch("/api/friends/add", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json"
                },
                body: JSON.stringify({
                    username: currentUsername,
                    friend_username: friendUsername
                })
            });
            const data = await response.json();

            if (response.ok) {
                alert(`已成功將${friendUsername}加入好友`);
                addFriendForm.elements.friend_username.value = "";
                loadFriends();
            } else {
                alert(data.error);
            }
        } catch (error) {
            alert("加好友失敗，請稍後再試");
        }
    });
});
