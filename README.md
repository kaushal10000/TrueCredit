# TrueCredit AI
**TrueCredit – Credit Card Recommendation System**

*Welcome to TrueCredit, an AI-powered chatbot that helps users discover the best credit cards tailored to their financial profile and lifestyle. Powered by Flask, Gemini AI (Gemini 2.5), and a curated database of Indian credit cards, TrueCredit simulates an intelligent assistant that understands user preferences and makes smart card suggestions.*



🌟 *Features*

✅ Conversational Interface – Chatbot-style interaction for ease of use

✅ Smart Parsing – Understands user inputs like income, spending habits, and preferences

✅ Dynamic Card Filtering – Recommends cards based on eligibility and user preferences

✅ Real-Time Responses – Powered by Gemini 2.5 for personalized suggestions

✅ Rich UI – Clean, responsive frontend with chat-like user experience

✅ Credit Card Database – Includes 25+ popular Indian credit cards with details and links



🧠 *How It Works*

The chatbot starts the conversation by asking for the user's monthly income.

It continues by collecting details like:

Spending habits (fuel, travel, groceries, etc.)

Preferred benefits (cashback, rewards, travel perks)

Existing credit cards

Credit score

Once all data is gathered, it uses Gemini AI to generate personalized credit card recommendations in a clean, structured format.



🛠️ *Setup Instructions*

1. Clone the Repository
bash

git clone https://github.com/your-username/truecredit.git

cd truecredit

2. Install Dependencies
   
Make sure you have Python 3.8+ and pip installed.

bash

pip install -r requirements.txt

If requirements.txt doesn't exist, install manually:

bash

pip install flask flask-cors python-dotenv google-generativeai

3. Set Up Environment Variables
   
Create a .env file in the root directory and add your Gemini API key:

env

GOOGLE_API_KEY=your_gemini_api_key_here

4. Run the App
bash

python app.py




💡 *Example Chat Flow*

🧠 AI: What's your monthly income?
👤 User: ₹50,000

🧠 AI: What are your main spending categories? (fuel, travel, groceries...)
👤 User: Travel and groceries

🧠 AI: What kind of benefits do you prefer? (cashback, rewards...)
👤 User: Cashback and airport lounge access

🧠 AI: Do you have any existing credit cards?
👤 User: SBI Card Prime

🧠 AI: What’s your approximate credit score?
👤 User: 770

🧠 AI: Here are the top 3 credit cards for you...



🖼️ *UI Preview*

![Screenshot 2025-06-19 223229](https://github.com/user-attachments/assets/3deba942-b72b-436a-af16-38eaca89c8da)
![Screenshot 2025-06-19 223350](https://github.com/user-attachments/assets/a6e11acb-a807-45dc-8aca-ce8018f3cda0)




