import os
from flask import Flask, request, jsonify
from flask_cors import CORS
from openai import OpenAI

app = Flask(__name__)
CORS(app)  # allows your GitHub Pages frontend to talk to this backend

client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

def load_knowledge_base() -> str:
    """Load the local knowledge base text file."""
    try:
        with open("knowledge_base.txt", "r", encoding="utf-8") as file:
            return file.read()
    except FileNotFoundError:
        return "No knowledge base file found."

@app.route("/chat", methods=["POST"])
def chat():
    data = request.get_json(silent=True) or {}
    user_message = data.get("message", "").strip()

    if not user_message:
        return jsonify({"reply": "Please type a message."}), 400

    knowledge_base = load_knowledge_base()

    system_prompt = f"""
You are a helpful chatbot.
Answer questions using the information below as your main knowledge base.
If the answer is not in the knowledge base, say you are not sure and ask the user to rephrase or add more information.

Knowledge Base:
{knowledge_base}
"""

    try:
        response = client.responses.create(
            model="gpt-5-mini",
            input=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_message}
            ]
        )

        return jsonify({"reply": response.output_text})

    except Exception as error:
        return jsonify({"reply": f"Error: {str(error)}"}), 500

@app.route("/", methods=["GET"])
def home():
    return jsonify({"status": "Backend is running."})

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=True)