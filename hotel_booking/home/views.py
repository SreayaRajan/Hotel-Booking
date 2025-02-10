from django.shortcuts import render, redirect


from django.contrib import messages
from django.contrib.auth.hashers import check_password
from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import authenticate, login as auth_login
from rest_framework.response import Response

from .models import *
from .serializers import RegisterSerializer
from rest_framework import status
from rest_framework.decorators import api_view

# from django.http import HttpResponse

def index(request):
    return render(request, 'index.html')

@api_view(['POST'])
def register(request):
    serializer = RegisterSerializer(data=request.data)

    if serializer.is_valid():
        user = serializer.save()
        login(request, user)  # Automatically log in after registration
        return Response({"message": "User registered successfully"}, status=status.HTTP_201_CREATED)

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# def loginn(request):
#     if request.method == "POST":
#         email = request.POST.get("email", "").strip()
#         password = request.POST.get("password", "").strip()
        
#         if not email or not password:
#             messages.error(request, "Email and password are required.")
#         else:
#             try:
#                 user = UserProfile.objects.get(email=email)
#                 if check_password(password, user.password):
#                     request.session["user_id"] = user.id  # Store user ID in session
#                     messages.success(request, f"Welcome, {user.first_name}!")
#                     return redirect("profile")  # Change 'profile' to the appropriate view name
#                 else:
#                     messages.error(request, "Invalid email or password.")
#             except UserProfile.DoesNotExist:
#                 messages.error(request, "Invalid email or password.")
    
#     form = AuthenticationForm()
#     return render(request, "login.html", {"form": form})
def loginn(request):
    # print('hi')
    # if request.method == 'POST':
    #     email = request.POST.get('email')
    #     password = request.POST.get('password')

    #     print("Trying to authenticate:", email, password)  # Debugging line

    #     # Authenticate using custom backend
    #     user = authenticate(request, email=email, password=password)
    #     print("Authentication result:", user)  # Debugging line

    #     if user:
    #         auth_login(request, user)  # Log the user in
    #         print("✅ User logged in:", user)
    #         return redirect('register')  # Redirect after login
    #     else:
    #         messages.error(request, 'Invalid email or password.')
    #         print("❌ Login failed")
    #         return redirect('login')

    return render(request, 'login.html')


def sucess(request):
    return render(request, 'sucess.html')