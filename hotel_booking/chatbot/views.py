# from django.http import JsonResponse
# from django.views.decorators.csrf import csrf_exempt
# import json
# import re

# # Predefined responses
# responses = {
#     "how to book": "To book, visit our website or app, choose a service, select a date and time, and confirm payment.",
#     "cancel booking": "To cancel a booking, go to 'My Bookings', select the booking, and click 'Cancel'. Cancellation fees may apply.",
#     "payment options": "We accept credit/debit cards, UPI, and net banking. EMI options are also available.",
#     "refund policy": "Refunds are processed within 5-7 business days based on the payment method used.",
#     "contact support": "You can contact our support team at support@example.com or call +1-800-123-4567."
# }

# # Function to get chatbot response
# def get_response(user_message):
#     user_message = user_message.lower()
    
#     for pattern, response in responses.items():
#         if re.search(pattern, user_message):
#             return response

#     return "I'm sorry, I didn't understand. Please ask about bookings, cancellations, or payments."

# @csrf_exempt  # Disable CSRF for API
# def chat(request):
#     if request.method == "POST":
#         try:
#             data = json.loads(request.body)
#             user_message = data.get("message", "")
#             response = get_response(user_message)
#             return JsonResponse({"response": response})
#         except json.JSONDecodeError:
#             return JsonResponse({"error": "Invalid JSON format"}, status=400)
#     return JsonResponse({"error": "Invalid request method"}, status=405)
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
import google.generativeai as genai  # Import Gemini API
import os
from dotenv import load_dotenv

# Load API Key
load_dotenv()
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")  # Update .env with Gemini API key

# Configure Gemini API
genai.configure(api_key=GEMINI_API_KEY)

# Function to get AI response
def get_ai_response(user_message):
    
    try:
        model = genai.GenerativeModel("gemini-pro")  # Use "gemini-pro" model
        response = model.generate_content(user_message)

        if response and response.text:
            return response.text.strip()
        else:
            return "I'm sorry, I couldn't generate a response."

    except Exception as e:
        print("Gemini API Error:", str(e))
        return "I'm having trouble understanding. Please try again later."

@csrf_exempt
def chat(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            user_message = data.get("message", "")

            if not user_message:
                return JsonResponse({"response": "Please enter a message."})

            response = get_ai_response(user_message)
            return JsonResponse({"response": response})

        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON format"}, status=400)

    return JsonResponse({"error": "Invalid request method"}, status=405)
