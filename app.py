from flask import Flask, render_template, request, jsonify
from google import genai
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)


def get_gemini_client():
    """Initialize Gemini client with API key from environment."""
    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        print("WARNING: GEMINI_API_KEY not found in environment variables")
        return None
    try:
        return genai.Client(api_key=api_key)
    except Exception as e:
        print(f"ERROR initializing Gemini client: {e}")
        return None


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
    """Handle chat requests from the frontend."""
    try:
        # Safely parse JSON request
        data = request.get_json(silent=True) or {}

        if not isinstance(data, dict):
            return jsonify({"error": "Invalid request payload."}), 400

        message = str(data.get("message", "")).strip()

        if not message:
            return jsonify({"error": "Please enter a message."}), 400

        # Check if client is initialized
        if client is None:
            return jsonify({
                "error": "Dino AI is not configured. Please set GEMINI_API_KEY environment variable."
            }), 500

        # Use configurable model name (default: gemini-2.0-flash)
        model_name = os.environ.get("GEMINI_MODEL", "gemini-2.0-flash")

        try:
            response = client.models.generate_content(
                model=model_name,
                contents=message
            )
        except Exception as model_error:
            print(f"Model error with {model_name}: {model_error}")
            # Fallback to gemini-1.5-flash if specified model fails
            try:
                response = client.models.generate_content(
                    model="gemini-1.5-flash",
                    contents=message
                )
            except Exception as fallback_error:
                print(f"Fallback model error: {fallback_error}")
                return jsonify({
                    "error": "Dino AI service is temporarily unavailable. Please try again."
                }), 503

        # Extract response text safely
        response_text = getattr(response, "text", None)
        if not response_text:
            return jsonify({
                "error": "Dino AI did not return a valid response. Please try again."
            }), 502

        return jsonify({"response": response_text})

    except Exception as e:
        print(f"AI ERROR: {e}")
        return jsonify({
            "error": "Dino AI encountered an error. Please try again later."
        }), 500


@app.errorhandler(404)
def not_found(error):
    """Handle 404 errors."""
    return jsonify({"error": "Page not found."}), 404


@app.errorhandler(500)
def internal_error(error):
    """Handle 500 errors."""
    return jsonify({"error": "Internal server error."}), 500


if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        port=5000,
        debug=True
    )
