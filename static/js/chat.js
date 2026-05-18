const chatForm = document.getElementById("chat-form");
const messageInput = document.getElementById("message-input");
const chatBox = document.getElementById("chat-box");

function addMessage(text, type) {
    const messageDiv = document.createElement("div");
    messageDiv.classList.add(type === "user" ? "user-message" : "bot-message");
    messageDiv.textContent = text;

    chatBox.appendChild(messageDiv);
    chatBox.scrollTop = chatBox.scrollHeight;
}

chatForm.addEventListener("submit", async function (event) {
    event.preventDefault();

    const message = messageInput.value.trim();

    if (!message) {
        return;
    }

    addMessage(message, "user");
    messageInput.value = "";

    try {
        const response = await fetch("/api/chat", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({
                message: message
            })
        });

        const data = await response.json();

        if (!response.ok) {
            addMessage(data.error || "오류가 발생했습니다.", "bot");
            return;
        }

        addMessage(data.answer, "bot");

    } catch (error) {
        addMessage("서버와 연결할 수 없습니다.", "bot");
        console.error(error);
    }
});