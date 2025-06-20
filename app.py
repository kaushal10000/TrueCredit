from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
import google.generativeai as genai
import os
import json
import re
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
CORS(app)

# ✅ Configure Gemini with API Key (no Client class)
genai.configure(api_key=os.environ["GOOGLE_API_KEY"])

# ✅ Initialize the Gemini model (e.g., Gemini 1.5 Flash)
model = genai.GenerativeModel("gemini-1.5-flash")

# Load credit card data
with open("cards.json", "r") as f:
    CARDS = json.load(f)

# ... [get_conversation_state and filter_cards unchanged] ...

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/chat", methods=["POST"])
def chat():
    try:
        data = request.get_json()
        messages = data.get("messages", [])
        state = get_conversation_state(messages)

        # Collect missing info step-by-step
        if not state["income"]:
            return jsonify({"reply": "What’s your monthly income?"})
        elif not state["habits"]:
            return jsonify({"reply": "What are your main spending categories? (fuel, travel, groceries, dining, shopping)"})
        elif not state["benefits"]:
            return jsonify({"reply": "What kind of benefits do you prefer? (cashback, rewards, travel points, airport lounge access, premium)"})
        elif not state["existing_cards"]:
            return jsonify({"reply": "Do you have any existing credit cards? If yes, which ones?"})
        elif not state["credit_score"]:
            return jsonify({"reply": "What’s your approximate credit score?"})

        # Construct prompt
        prompt = (
            f"User profile:\n"
            f"- Income: ₹{state['income']:,}/month\n"
            f"- Spending habits: {', '.join(state['habits'])}\n"
            f"- Benefits preferred: {', '.join(state['benefits'])}\n"
            f"- Existing cards: {state['existing_cards']}\n"
            f"- Credit score: {state['credit_score']}\n\n"
            f"Based on the above, please provide a concise list of the top 3 suitable credit cards.\n"
            f"Use this format:\n"
            f"**Card Name** by Issuer: Reward Type\n"
            f"- Features: feature1, feature2\n"
            f"- Apply: [link]\n\n"
        )

        # ✅ Use the generative model correctly
        response = model.generate_content(prompt)

        return jsonify({"reply": response.text})

    except Exception as e:
        return jsonify({"reply": f"❌ Something went wrong: {str(e)}"}), 500

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
