import google.generativeai as genai
import os
from dotenv import load_dotenv

# Load API key
load_dotenv()
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
genai.configure(api_key=GEMINI_API_KEY)

# Generate AI response
try:
    model = genai.GenerativeModel("gemini-pro")
    response = model.generate_content("How do I book a hotel?")
    print("Response:", response.text)
except Exception as e:
    print("Gemini API Error:", str(e))
