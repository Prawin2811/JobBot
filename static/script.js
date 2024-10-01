document.addEventListener("DOMContentLoaded", function () {
    const chatBox = document.querySelector("#chat-box");
    const inputField = document.querySelector("#user-input");
    const sendButton = document.querySelector("#send-btn");
    const clearButton = document.querySelector("#clear-btn");
    const uploadButton = document.querySelector("#upload-btn");
    const uploadInput = document.querySelector("#upload");

    function addMessage(content, type) {
        const messageDiv = document.createElement("div");
        messageDiv.classList.add("message", type);
        messageDiv.innerHTML = content;  // Use innerHTML to allow HTML formatting
        chatBox.appendChild(messageDiv);
        chatBox.scrollTop = chatBox.scrollHeight;
    }

    function handleSendMessage() {
        const message = inputField.value.trim();
        if (message) {
            addMessage(message, "user");
            inputField.value = "";

            fetch("/api/chat", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                },
                body: JSON.stringify({ message }),
            })
            .then(response => response.json())
            .then(data => {
                addMessage(data.response, "bot");
            })
            .catch(error => {
                console.error("Error:", error);
                addMessage("Sorry, something went wrong.", "bot");
            });
        }
    }

    sendButton.addEventListener("click", handleSendMessage);

    inputField.addEventListener("keydown", function (event) {
        if (event.key === "Enter" && !event.shiftKey) {
            event.preventDefault();
            handleSendMessage();
        }
    });

    clearButton.addEventListener("click", function () {
        chatBox.innerHTML = "";
    });

    uploadButton.addEventListener("click", function () {
        const file = uploadInput.files[0];
        if (file && file.type === "application/pdf") {
            const formData = new FormData();
            formData.append("file", file);

            fetch("/api/upload", {
                method: "POST",
                body: formData,
            })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    addMessage("PDF uploaded successfully. You can now ask questions about the resume.", "bot");
                } else {
                    addMessage("Error processing the PDF.", "bot");
                }
            })
            .catch(error => {
                addMessage("Sorry, something went wrong while uploading the PDF.", "bot");
                console.error("Error:", error);
            });
        } else {
            addMessage("Please upload a valid PDF file.", "bot");
        }
    });
});
