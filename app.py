from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
from google import genai
import os
import json
import re
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
CORS(app)

# Initialize the GenAI client globally
client = genai.Client()

# Load credit card data
with open("cards.json", "r") as f:
    CARDS = json.load(f)

def get_conversation_state(messages):
    state = {
        "income": None,
        "habits": [],
        "benefits": [],
        "existing_cards": None,
        "credit_score": None
    }

    for m in messages:
        if m["role"] != "user":
            continue
        content = m["content"].lower()

        # Extract income
        if not state["income"]:
            match = re.search(r'(?:₹|rs\.?)?\s?([\d,]+(?:\.\d+)?)(\s?(?:[lLkK]|lakhs?|thousands?)?)', content)
            if match:
                num_str, unit = match.groups()
                try:
                    num = float(num_str.replace(",", ""))
                    unit = unit.strip().lower()
                    multiplier = 1
                    if unit in ['l', 'lakh', 'lakhs']:
                        multiplier = 100000
                    elif unit in ['k', 'thousand']:
                        multiplier = 1000
                    state["income"] = int(num * multiplier)
                except ValueError:
                    pass

        # Habits
        for keyword in ["fuel", "travel", "groceries", "dining", "shopping"]:
            if keyword in content and keyword not in state["habits"]:
                state["habits"].append(keyword)

        # Benefits
        for keyword in ["cashback", "rewards", "lounge", "miles", "travel points", "airport", "premium"]:
            if keyword in content and keyword not in state["benefits"]:
                state["benefits"].append(keyword)

        # Existing cards
        if not state["existing_cards"]:
            if re.search(r'\b(no|none|nope|not at all|never)\b', content):
                state["existing_cards"] = "None"
            else:
                issuers = ["hdfc", "sbi", "axis", "icici", "federal", "kotak", "yes", "amex", "idfc", "indusind", "bob"]
                for issuer in issuers:
                    if issuer in content:
                        state["existing_cards"] = issuer
                        break
                if not state["existing_cards"] and re.search(r'\b(card|credit)\b', content):
                    state["existing_cards"] = content

        # Credit score
        if not state["credit_score"]:
            match = re.search(r'(\d{3})', content)
            if match:
                score = int(match.group(1))
                if 300 <= score <= 900:
                    state["credit_score"] = score

    return state

def filter_cards(user_income: int, preference_keywords: list):
    matched = []
    for card in CARDS:
        min_income = card.get("eligibility", {}).get("min_income", 0)
        if user_income < min_income:
            continue

        reward_type = card.get("reward_type", "").lower()
        features = " ".join(card.get("features", [])).lower()

        if any(
            keyword.lower() in reward_type or
            keyword.lower() in features
            for keyword in preference_keywords
        ):
            matched.append(card)
    return matched

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

        # Prepare prompt with your custom instructions
        prompt = (
            f"User profile:\n"
            f"- Income: ₹{state['income']:,}/month\n"
            f"- Spending habits: {', '.join(state['habits'])}\n"
            f"- Benefits preferred: {', '.join(state['benefits'])}\n"
            f"- Existing cards: {state['existing_cards']}\n"
            f"- Credit score: {state['credit_score']}\n\n"
            f"Based on the above, please provide a **concise, clear, and well-structured** list of the top 3 suitable credit cards.\n"
            f"Use bullet points, include card name, issuer, reward type, key features, and application link. Each credit card should be clearly separated with space, and the credit card name should be bold.\n"
            f"Example format:\n"
            f"- Card Name by Issuer: Reward Type\n"
            f"  - Features: feature1, feature2, ...\n"
            f"  - Apply: [link]\n\n"
            f"Please ensure there is a space between each recommendation for clarity."
        )

        # Generate content using Gemini 2.5 flash model
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt
        )

        return jsonify({"reply": response.text})

    except Exception as e:
        return jsonify({"reply": f"❌ Something went wrong: {str(e)}"}), 500

if __name__ == "__main__":
    app.run(debug=True)
