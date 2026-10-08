from flask import Flask, render_template, request, jsonify
from google import genai
import os

app = Flask(__name__)


def get_gemini_client():
    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        return None
    return genai.Client(api_key=api_key)


client = get_gemini_client()


@app.route("/")
def home():
    return render_template("codewithdino.html")


@app.route("/course")
def course():
    return render_template("courses.html")


@app.route("/home")
def about():
    return render_template("codewithdino.html")


@app.route("/roadmap")
def roadmap():
    return render_template("roadmap.html")


@app.route("/aibot")
def aibot():
    return render_template("dinoai.html")


@app.route("/api/chat", methods=["POST"])
def chat():
    try:
        data = request.get_json(silent=True) or {}

        if not isinstance(data, dict):
            return jsonify({"error": "Invalid request payload."}), 400

        message = str(data.get("message", "")).strip()

        if not message:
            return jsonify({"error": "Please enter a message."}), 400

        if client is None:
            return jsonify({"error": "Dino AI is not configured. Please set GEMINI_API_KEY."}), 500

        model_name = os.environ.get("GEMINI_MODEL", "gemini-2.0-flash")
        response = client.models.generate_content(
            model=model_name,
            contents=message
        )

        response_text = getattr(response, "text", None)
        if not response_text:
            return jsonify({"error": "Dino AI did not return a valid response."}), 500

        return jsonify({"response": response_text})

    except Exception as e:
        print("AI ERROR:", e)
        return jsonify({"error": "Dino AI could not generate a response."}), 500


if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        port=5000,
        debug=True
    )
