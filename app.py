import os
from pathlib import Path

from flask import Flask, request, jsonify
from flask_cors import CORS
from openai import OpenAI


app = Flask(__name__)
CORS(app)

client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

BASE_DIR = Path(__file__).resolve().parent
KNOWLEDGE_BASE_FILE = BASE_DIR / "knowledge_base.txt"


def load_knowledge_base() -> str:
    """Load the knowledge base stored beside app.py."""
    try:
        knowledge = KNOWLEDGE_BASE_FILE.read_text(encoding="utf-8")

        if not knowledge.strip():
            print("WARNING: knowledge_base.txt is empty.")
            return "The knowledge base is currently empty."

        print(f"Knowledge base loaded: {len(knowledge)} characters")
        return knowledge

    except FileNotFoundError:
        print(f"ERROR: Knowledge base not found at {KNOWLEDGE_BASE_FILE}")
        return "No knowledge base file was found."

    except OSError as error:
        print(f"ERROR: Could not read knowledge base: {error}")
        return "The knowledge base could not be loaded."


@app.route("/chat", methods=["POST"])
def chat():
    data = request.get_json(silent=True) or {}
    user_message = data.get("message", "").strip()

    if not user_message:
        return jsonify({"reply": "Please type a message."}), 400

    if len(user_message) > 500:
        return jsonify({
            "reply": "Please shorten your message to 500 characters or fewer."
        }), 400

    knowledge_base = load_knowledge_base()

    system_prompt = f"""
You are a helpful support chatbot.

Use the knowledge base below as your primary and authoritative source.

Instructions:
- Read the full knowledge base before answering.
- If the answer is present, answer clearly using that information.
- Do not claim information is missing if it is included in the knowledge base.
- Do not invent facts, contact details, policies or procedures.
- If the answer genuinely is not present, say:
  "I could not find that information in the available knowledge base."
- Keep answers concise and easy to understand.

KNOWLEDGE BASE START
--------------------
{knowledge_base}
--------------------
KNOWLEDGE BASE END
"""

    try:
        response = client.responses.create(
            model="gpt-5-mini",
            instructions=system_prompt,
            input=user_message
        )

        return jsonify({"reply": response.output_text})

    except Exception as error:
        print(f"OpenAI request failed: {error}")

        return jsonify({
            "reply": "The chatbot could not process your request right now."
        }), 500


@app.route("/", methods=["GET"])
def home():
    return jsonify({"status": "Backend is running."})


@app.route("/knowledge-status", methods=["GET"])
def knowledge_status():
    knowledge = load_knowledge_base()

    return jsonify({
        "file_exists": KNOWLEDGE_BASE_FILE.exists(),
        "file_name": KNOWLEDGE_BASE_FILE.name,
        "character_count": len(knowledge),
        "preview": knowledge[:300]
    })


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=False)
