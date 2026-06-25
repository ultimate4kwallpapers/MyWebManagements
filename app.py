import os
from flask import Flask, request, jsonify
from flask_cors import CORS
import google.generativeai as genai

# Server Setup
app = Flask(__name__)
# Allow Blogger to request data from this server
CORS(app) 

# Gemini API Configuration 
# (Hum API key ko environment variable me hide karenge security ke liye)
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY")
genai.configure(api_key=GEMINI_API_KEY)

# Gemini 1.5 Flash - Super fast and free tier friendly
model = genai.GenerativeModel('gemini-1.5-flash')

# ----------------------------------------------------
# ROUTE 1: Semantic Search Analyzer (The Brain)
# ----------------------------------------------------
@app.route('/api/analyze-query', methods=['POST'])
def analyze_query():
    try:
        # Get data from Blogger Frontend
        data = request.get_json()
        user_query = data.get('query', '')

        if not user_query:
            return jsonify({"error": "Query is missing"}), 400

        # AI Prompt: Instructing Gemini to understand the search
        prompt = f"""
        You are a backend search engine for an anime, gaming, and aesthetic wallpaper website.
        A user just searched for this text: "{user_query}"
        
        Your job is to understand the intent and map it to our existing categories/tags.
        Our Main Tags are: Anime, Gaming, Nature, Cars, Aesthetic, Manhwa, Dark, Cyberpunk, Setup, 4K.
        
        Return ONLY a comma-separated list of the 3 best matching tags for this search. 
        Do not add any other text.
        """

        # Call Gemini API
        response = model.generate_content(prompt)
        
        # Clean the response into an array
        tags_string = response.text.strip()
        cleaned_tags = [tag.strip() for tag in tags_string.split(',')]

        # Send response back to Blogger
        return jsonify({
            "status": "success",
            "original_query": user_query,
            "suggested_tags": cleaned_tags
        }), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500

# ----------------------------------------------------
# ROUTE 2: Server Health Check
# ----------------------------------------------------
@app.route('/', methods=['GET'])
def home():
    return "Ultimate 4K Wallpapers AI Backend is Running Securely! 🚀"

# Start the Server
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)