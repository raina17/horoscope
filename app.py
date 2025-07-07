# In app.py

import os
from flask import Flask, request, jsonify, render_template
from openai import AzureOpenAI
from datetime import datetime
from dotenv import load_dotenv

# Load environment variables from a .env file for local development
load_dotenv()

app = Flask(__name__, static_folder='static', template_folder='templates')

# --- Azure OpenAI Configuration ---
# It's best practice to use environment variables for keys and endpoints
# For Azure deployment, these will be set in the App Service Configuration
AZURE_OPENAI_ENDPOINT = os.getenv("AZUREOPENAIENDPOINT")
AZURE_OPENAI_KEY = os.getenv("AZUREOPENAIKEY")
AZURE_OPENAI_API_VERSION = "2024-02-01" # Use a recent, stable version
AZURE_OPENAI_DEPLOYMENT_NAME = os.getenv("AZUREOPENAIDEPLOYMENTNAME")

# Initialize the Azure OpenAI client
client = AzureOpenAI(
    azure_endpoint=AZURE_OPENAI_ENDPOINT,
    api_key=AZURE_OPENAI_KEY,
    api_version=AZURE_OPENAI_API_VERSION
)

# --- Zodiac Sign Calculation Helper ---
def get_zodiac_sign(day, month):
    if month == 12:
        return 'Sagittarius' if (day < 22) else 'Capricorn'
    elif month == 1:
        return 'Capricorn' if (day < 20) else 'Aquarius'
    elif month == 2:
        return 'Aquarius' if (day < 19) else 'Pisces'
    elif month == 3:
        return 'Pisces' if (day < 21) else 'Aries'
    elif month == 4:
        return 'Aries' if (day < 20) else 'Taurus'
    elif month == 5:
        return 'Taurus' if (day < 21) else 'Gemini'
    elif month == 6:
        return 'Gemini' if (day < 21) else 'Cancer'
    elif month == 7:
        return 'Cancer' if (day < 23) else 'Leo'
    elif month == 8:
        return 'Leo' if (day < 23) else 'Virgo'
    elif month == 9:
        return 'Virgo' if (day < 23) else 'Libra'
    elif month == 10:
        return 'Libra' if (day < 23) else 'Scorpio'
    elif month == 11:
        return 'Scorpio' if (day < 22) else 'Sagittarius'

# --- API Endpoint to Generate Horoscope ---
@app.route('/generate-horoscope', methods=['POST'])
def generate_horoscope():
    try:
        data = request.json
        name = data.get('name')
        dob_str = data.get('dob')
        place_of_birth = data.get('placeOfBirth')
        gender = data.get('gender')

        if not all([name, dob_str, place_of_birth, gender]):
            return jsonify({"error": "Missing required fields"}), 400

        # Calculate Zodiac Sign
        dob_date = datetime.strptime(dob_str, '%Y-%m-%d')
        zodiac_sign = get_zodiac_sign(dob_date.day, dob_date.month)

        # --- Prompt Engineering: The Key to a Good Response ---
        # We instruct the AI to act as an astrologer and return a JSON object.
        prompt_message = f"""
        You are a professional and insightful astrologer.
        A user named {name} ({gender}), born on {dob_str} in {place_of_birth}, wants their horoscope.
        Their zodiac sign is {zodiac_sign}.

        Based on this information, please generate a personalized horoscope.
        Provide predictions for the following three timeframes:
        1. Daily Horoscope: For today.
        2. Weekly Horoscope: For the current week.
        3. Monthly Horoscope: For the current month.

        Keep the tone positive, inspiring, and engaging. Focus on key life areas like love, career, finance, and health.

        IMPORTANT: Please format your entire response as a single, clean JSON object with three keys: "daily", "weekly", and "monthly". Do not include any text or explanations outside of the JSON object.

        Example JSON format:
        {{
          "daily": "Today is a day of...",
          "weekly": "This week you will find...",
          "monthly": "The month ahead holds..."
        }}
        """

        # --- Call the Azure OpenAI API ---
        response = client.chat.completions.create(
            model=AZURE_OPENAI_DEPLOYMENT_NAME,
            messages=[
                {"role": "system", "content": "You are an expert astrologer who provides responses in JSON format."},
                {"role": "user", "content": prompt_message}
            ],
            temperature=0.7,  # A bit of creativity
            max_tokens=2000,
            top_p=0.95,
            frequency_penalty=0,
            presence_penalty=0
        )

        horoscope_data = response.choices[0].message.content
        
        # The AI should return a JSON string, so we return it directly.
        # For robustness, you might want to parse and validate it, but for this example, we'll keep it simple.
        return horoscope_data, 200, {'Content-Type': 'application/json'}

    except Exception as e:
        print(f"An error occurred: {e}")
        return jsonify({"error": "Failed to generate horoscope. " + str(e)}), 500

# --- Route to Serve the Frontend ---
@app.route('/')
def index():
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
