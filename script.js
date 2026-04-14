const chatBox = document.getElementById("chat-box");
const userInput = document.getElementById("user-input");
const sendBtn = document.getElementById("send-btn");

// Replace this with your Render backend URL after deployment
const API_URL = "https://ai-chatbot-backend-0e8f.onrender.com/";

function addMessage(text, sender) {
  const msg = document.createElement("div");
  msg.classList.add("message", sender);
  msg.textContent = text;
  chatBox.appendChild(msg);
  chatBox.scrollTop = chatBox.scrollHeight;
}

async function sendMessage() {
  const message = userInput.value.trim();
  if (!message) return;

  addMessage(message, "user");
  userInput.value = "";

  addMessage("Typing...", "bot");
  const typingMessage = chatBox.lastChild;

  try {
    const response = await fetch(API_URL, {
      method: "POST",
      headers: {
        "Content-Type": "application/json"
      },
      body: JSON.stringify({ message })
    });

    const data = await response.json();
    typingMessage.textContent = data.reply || "No response received.";
  } catch (error) {
    typingMessage.textContent = "Sorry, something went wrong connecting to the chatbot.";
  }
}

sendBtn.addEventListener("click", sendMessage);

userInput.addEventListener("keypress", function (event) {
  if (event.key === "Enter") {
    sendMessage();
  }
});
