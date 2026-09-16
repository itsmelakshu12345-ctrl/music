import os
from flask import Flask, jsonify, render_template, request
from dotenv import load_dotenv
from google import genai
from chatbot_config import SYSTEM_PROMPT

load_dotenv()

app = Flask(__name__)

api_key = os.getenv("GEMINI_API_KEY")
if not api_key:
    raise ValueError("GEMINI_API_KEY is missing.")

client = genai.Client(api_key=api_key)
MODEL_NAME = "gemini-3.1-flash-lite"


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/chat", methods=["POST"])
def chat():
    data = request.get_json(silent=True) or {}
    message = data.get("message", "").strip()

    if not message:
        return jsonify({"reply": "Please enter a study-related question."})

    try:
        response = client.models.generate_content(
            model=MODEL_NAME,
            contents=message,
            config={"system_instruction": SYSTEM_PROMPT}
        )
        return jsonify({"reply": response.text or "No response received."})
    except Exception:
        return jsonify({
            "reply": "Sorry, I could not process your question right now."
        }), 500


if __name__ == "__main__":
    app.run(debug=True)
