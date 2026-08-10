const input = document.getElementById("user-input");
const chatBox = document.getElementById("chat-box");
const characterCount = document.getElementById("character-count");
const sendButton = document.getElementById("send-button");


/* --------------------------------
   Character counter
   -------------------------------- */

input.addEventListener("input", function () {

    characterCount.textContent =
        `${input.value.length} / 500 characters`;

});


/* --------------------------------
   Press Enter to send
   Shift + Enter = new line
   -------------------------------- */

input.addEventListener("keydown", function (event) {

    if (event.key === "Enter" && !event.shiftKey) {

        event.preventDefault();

        sendMessage();

    }

});


/* --------------------------------
   Add message to chat window
   -------------------------------- */

function addMessage(message, sender) {

    const row = document.createElement("div");

    row.classList.add("message-row");


    const bubble = document.createElement("div");

    bubble.classList.add("message");


    if (sender === "user") {

        row.classList.add("user-row");

        bubble.classList.add("user-message");

    } else {

        row.classList.add("bot-row");


        const icon = document.createElement("div");

        icon.classList.add("bot-icon");

        icon.textContent = "🤖";


        row.appendChild(icon);


        bubble.classList.add("bot-message");

    }


    bubble.textContent = message;

    row.appendChild(bubble);

    chatBox.appendChild(row);


    chatBox.scrollTop = chatBox.scrollHeight;

}


/* --------------------------------
   Send message
   -------------------------------- */

async function sendMessage() {

    const message = input.value.trim();


    if (!message) {

        addMessage(
            "Please type a question before sending.",
            "bot"
        );

        return;

    }


    if (message.length > 500) {

        addMessage(
            "Please shorten your message to 500 characters or fewer.",
            "bot"
        );

        return;

    }


    addMessage(message, "user");


    input.value = "";

    characterCount.textContent = "0 / 500 characters";


    sendButton.disabled = true;

    sendButton.textContent = "Sending...";


    try {

        /*
        IMPORTANT:
        Replace the URL below with the SAME
        Render /chat URL currently used in your
        existing working script.js.
        */

        const response = await fetch(
            "https://ai-chatbot-backend-0e8f.onrender.com/chat",
            {
                method: "POST",

                headers: {
                    "Content-Type": "application/json"
                },

                body: JSON.stringify({
                    message: message
                })
            }
        );


        const data = await response.json();


        if (!response.ok) {

            addMessage(
                data.reply ||
                "Sorry, something went wrong.",
                "bot"
            );

            return;

        }


        addMessage(data.reply, "bot");


    } catch (error) {

        console.error(error);


        addMessage(
            "Sorry, I couldn't connect to the chatbot. Please try again.",
            "bot"
        );

    } finally {

        sendButton.disabled = false;

        sendButton.innerHTML =
            '<span aria-hidden="true">➤</span> Send';

        input.focus();

    }

}
