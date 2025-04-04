
from django.contrib import messages
from django.contrib.auth.hashers import make_password
# from home.models import UserProfile
from django.contrib.auth.hashers import check_password
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from .models import * 
import razorpay
from django.conf import settings
from django.http import JsonResponse
from django.core.mail import send_mail
from django.contrib.auth import logout


# @login_required
def index(request):
    return render(request, 'index.html')

@login_required
def room(request):
    rooms = Room.objects.all()  # Fetch all rooms
    return render(request, 'room.html', {'rooms': rooms})
@login_required
def room_detail(request, room_id):
    room = get_object_or_404(Room, id=room_id)
    return render(request, 'room_detail.html', {'room': room})

def service(request):
    return render(request, 'service.html')
def team(request):
    return render(request, 'team.html')
def testmonial(request):
    return render(request, 'testmonial.html')
def about(request):
    return render(request, 'about.html')

def register(request):
    if request.method == "POST":
        # Retrieve form data
        username = request.POST.get("username")
        email = request.POST.get("email")
        phone_number = request.POST.get("number")  # Match model field name
        password = request.POST.get("password")

        # Check for duplicate username, email, or phone number
        if UserProfile.objects.filter(username=username).exists():
            messages.error(request, "Username already taken")
            return redirect("register")

        if UserProfile.objects.filter(email=email).exists():
            messages.error(request, "Email already in use")
            return redirect("register")

        if UserProfile.objects.filter(number=phone_number).exists():
            messages.error(request, "Phone number already in use")
            return redirect("register")

        # Create and save the user with a hashed password
        # UserProfile.objects.create(
        #     username=username,
        #     email=email,
        #     number=phone_number,
        #     password=make_password(password)  # Hashing password before saving
        # )
        
        hashed_password = make_password(password)  # Hash the password before saving

        user = UserProfile(username=username, email=email,number=phone_number, password=hashed_password)
        user.save()

        messages.success(request, "Registration successful! You can now log in.")
        return redirect("login")  # Redirect to login page

    return render(request, "register.html")  # Handle GET request properly


def loginn(request):
    if request.method == "POST":
        email = request.POST.get("email")
        password = request.POST.get("password")

        try:
            user_profile = UserProfile.objects.get(email=email)
        except UserProfile.DoesNotExist:
            messages.error(request, "User does not exist.")
            return redirect("login")

        if check_password(password, user_profile.password):  
            request.session['user_id'] = user_profile.id  
            request.session['username'] = user_profile.username  
            
            # 🔹 Make Django recognize this user as logged in
            user_profile.backend = 'django.contrib.auth.backends.ModelBackend'  # Required for login()
            login(request, user_profile)

            messages.success(request, f"Welcome, {user_profile.username}! You have successfully logged in.")
            return redirect("index")  # Redirect to the hotel room page
        else:
            messages.error(request, "Invalid email or password.")
            return redirect("login")

    return render(request, "login.html")

def user_logout(request):
    logout(request) 
    return redirect('login') 


@login_required
def booking_page(request, room_id):
    room = get_object_or_404(Room, id=room_id)
    return render(request, 'booking.html', {'room': room})

@login_required
def book_room(request, room_id):
    room = get_object_or_404(Room, id=room_id)

    if request.method == "POST":
        checkin = request.POST.get("checkin")
        checkout = request.POST.get("checkout")

        if not checkin or not checkout:
            messages.error(request, "Please fill in all required fields.")
            return redirect('book_room', room_id=room.id)

        try:
            # Create Booking Entry (Initially Unpaid)
            booking = Booking.objects.create(
                user=request.user,
                room=room,
                location=room.location,
                category=room.subcategory.category,
                subcategory=room.subcategory,
                amount=room.room_rent,
                checkin=checkin,
                checkout=checkout
            )

            # Initialize Razorpay Client
            client = razorpay.Client(auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET))

            # Create Razorpay Order
            order_data = {
                "amount": int(room.room_rent * 100),  # Convert amount to paise
                "currency": "INR",
                "receipt": str(booking.booking_id),
                "payment_capture": 1  # Auto-capture payment
            }
            razorpay_order = client.order.create(order_data)

            # After successful order creation, update the payment_method in the booking model
            booking.payment_method = 'razorpay'
            booking.save()

            return JsonResponse({
                "razorpay_key": settings.RAZORPAY_KEY_ID,
                "amount": order_data["amount"],
                "currency": order_data["currency"],
                "razorpay_order_id": razorpay_order["id"],
                "booking_id": str(booking.booking_id)
            })

        except Exception as e:
            print(f"Error creating booking: {e}")
            messages.error(request, "An error occurred while processing your booking.")
            return redirect('book_room', room_id=room.id)

    return render(request, 'room.html', {"room": room})


@login_required
def booking_success(request, booking_id):
    booking = get_object_or_404(Booking, booking_id=booking_id)
    return render(request, 'success.html', {'booking': booking})


def contact(request):
    if request.method == "POST":
        name = request.POST.get("name")
        email = request.POST.get("email")
        subject = request.POST.get("subject")
        message = request.POST.get("message")
        
        # If the user is authenticated, link the message to the user
        user = request.user if request.user.is_authenticated else None

        # Save to database
        contact = Contact.objects.create(
            user=user,
            name=name,
            email=email,
            subject=subject,
            message=message
        )

        # Send email to the owner
        owner_email = "sreayarajan75@gmail.com"  # ✅ Your email as the recipient

        try:
            send_mail(
                f"New Contact Form Submission: {subject}",
                f"From: {name} ({email})\n\nMessage:\n{message}",
                "sreayarajan75@gmail.com",  # ✅ Use your own email as the sender (EMAIL_HOST_USER)
                [owner_email],  # ✅ Send to your own email
                fail_silently=False,
            )
            messages.success(request, "Your message has been sent successfully!")
        except Exception as e:
            messages.error(request, f"Error sending email: {e}")

        return redirect("contact")  # Redirect to the contact page after submission

    return render(request, "contact.html")
#ADMIN SIDE
def index1(request):
    return render(request, 'adminside/index1.html')

def admin_login(request):
    if request.method == "POST":
        email = request.POST.get("email")  # Change to email
        password = request.POST.get("password")

        user = authenticate(request, email=email, password=password)  # Authenticate with email

        if user is not None and user.is_superuser:  # Ensure only superusers can log in
            login(request, user)
            return redirect("index1")  # Redirect to the admin dashboard
        else:
            messages.error(request, "Invalid credentials or not an admin.")

    return render(request, "adminside/admin_login.html")

def admin_logout(request):
    request.session.flush()  # Clears all session data
    logout(request)  # Logs out the user
    return redirect("admin_login") 
@login_required

def dashboard(request):
    return render(request, "adminside/dashboard.html")
@login_required(login_url="admin_login")
def manage_location(request):
    if request.method == "POST":
        if "location_id" in request.POST:  # If updating
            location_id = request.POST.get("location_id")
            location_name = request.POST.get("location_name")
            location = get_object_or_404(Location, id=location_id)
            location.location_name = location_name
            location.save()
        elif "delete_id" in request.POST:  # If deleting
            location_id = request.POST.get("delete_id")
            location = get_object_or_404(Location, id=location_id)
            location.delete()
        else:  # If creating a new location
            location_name = request.POST.get("location_name")
            if location_name:
                Location.objects.create(location_name=location_name)

        return redirect("manage_location")

    locations = Location.objects.all()
    return render(request, "adminside/location.html", {"locations": locations})

def manage_category(request):
    locations = Location.objects.all()
    categories = Category.objects.select_related('location_name').all()

    if request.method == 'POST':
        if 'add_category' in request.POST:
            location_id = request.POST.get('location_id')
            category_name = request.POST.get('category_name')
            if location_id and category_name:
                location = Location.objects.get(id=location_id)
                Category.objects.create(location_name=location, category_name=category_name)
                return redirect('manage_category')

        elif 'update_category' in request.POST:
            category_id = request.POST.get('category_id')
            category_name = request.POST.get('category_name')
            category = Category.objects.get(id=category_id)
            category.category_name = category_name
            category.save()
            return redirect('manage_category')

        elif 'delete_category' in request.POST:
            category_id = request.POST.get('delete_id')
            Category.objects.get(id=category_id).delete()
            return redirect('manage_category')

    return render(request, 'adminside/category.html', {'locations': locations, 'categories': categories})


def manage_category(request):
    locations = Location.objects.all()
    categories = Category.objects.select_related('location_name').all()

    if request.method == 'POST':
        if 'add_category' in request.POST:
            location_id = request.POST.get('location_id')
            category_name = request.POST.get('category_name')
            location = get_object_or_404(Location, id=location_id)
            Category.objects.create(location_name=location, category_name=category_name)
            return redirect('manage_category')

        elif 'update_category' in request.POST:
            category_id = request.POST.get('category_id')
            category_name = request.POST.get('category_name')
            category = get_object_or_404(Category, id=category_id)
            category.category_name = category_name
            category.save()
            return redirect('manage_category')

        elif 'delete_category' in request.POST:
            delete_id = request.POST.get('delete_id')
            Category.objects.filter(id=delete_id).delete()
            return redirect('manage_category')

    return render(request, 'adminside/category.html', {
        'locations': locations,
        'categories': categories,
    })

def manage_category(request):
    locations = Location.objects.all()
    categories = Category.objects.select_related('location_name').all()

    if request.method == 'POST':
        if 'add_category' in request.POST:
            location_id = request.POST.get('location_id')
            category_name = request.POST.get('category_name')
            location = get_object_or_404(Location, id=location_id)
            Category.objects.create(location_name=location, category_name=category_name)
            return redirect('manage_category')

        elif 'update_category' in request.POST:
            category_id = request.POST.get('category_id')
            category_name = request.POST.get('category_name')
            category = get_object_or_404(Category, id=category_id)
            category.category_name = category_name
            category.save()
            return redirect('manage_category')

        elif 'delete_category' in request.POST:
            delete_id = request.POST.get('delete_id')
            Category.objects.filter(id=delete_id).delete()
            return redirect('manage_category')

    return render(request, 'adminside/category.html', {
        'locations': locations,
        'categories': categories,
    })


def manage_subcategory(request, category_id):
    category = get_object_or_404(Category, id=category_id)
    location = category.location_name
    subcategories = SubCategory.objects.filter(category=category)

    if request.method == 'POST':
        subcategory_name = request.POST.get('subcategory_name')

        if 'add_subcategory' in request.POST and subcategory_name:
            # ✅ Add new subcategory
            SubCategory.objects.create(
                category=category,
                subcategory_name=subcategory_name
            )
            return redirect('manage_subcategory', category_id=category_id)

        elif 'update_subcategory' in request.POST:
            subcategory_id = request.POST.get('subcategory_id')
            subcategory = get_object_or_404(SubCategory, id=subcategory_id)
            subcategory.subcategory_name = subcategory_name
            subcategory.save()
            return redirect('manage_subcategory', category_id=category_id)

        elif 'delete_subcategory' in request.POST:
            subcategory_id = request.POST.get('delete_id')
            SubCategory.objects.filter(id=subcategory_id).delete()
            return redirect('manage_subcategory', category_id=category_id)

    return render(request, 'adminside/subcategory.html', {
        'category': category,
        'location': location,
        'subcategories': subcategories,
    })
    

def room_details(request):
    if request.method == "POST":
        if "delete_room" in request.POST:
            room_id = request.POST.get("delete_id")
            room = get_object_or_404(Room, id=room_id)
            room.images.all().delete()  # Delete related images
            room.delete()
            return redirect("room_details")

    rooms = Room.objects.all()
    return render(request, "adminside/room__details.html", {"rooms": rooms})


# def manage_room(request):
#     selected_location_id = request.GET.get("location", "")  # Get selected location from request
#     locations = Location.objects.all()
    
#     # Fetch only the subcategories related to the selected location
#     if selected_location_id:
#         subcategories = SubCategory.objects.filter(location_id=selected_location_id)
#     else:
#         subcategories = SubCategory.objects.none()  # Show empty initially
    
#     if request.method == "POST":
#         if "add_room" in request.POST:
#             subcategory_id = request.POST.get("subcategory")
#             location_id = request.POST.get("location")
#             room_rent = request.POST.get("room_rent")
#             room_details = request.POST.get("room_details")
#             available_room = request.POST.get("available_room")
#             room_images = request.FILES.getlist("room_images")  # Get multiple files

#             subcategory = get_object_or_404(SubCategory, id=subcategory_id)
#             location = get_object_or_404(Location, id=location_id)

#             # Create the Room instance
#             room = Room.objects.create(
#                 subcategory=subcategory,
#                 location=location,
#                 room_rent=room_rent,
#                 room_details=room_details,
#                 available_room=available_room,
#             )

#             # Save multiple images linked to the room
#             for image in room_images:
#                 RoomImage.objects.create(room=room, image=image)

#             return redirect("room_rate")

#     return render(
#         request,
#         "adminside/room_rate.html",
#         {
#             "locations": locations,
#             "subcategories": subcategories,
#             "selected_location_id": selected_location_id,
#         },
#     )


def manage_room(request):
    # Get selected location from request (either POST or GET)
    selected_location_id = request.POST.get("location") or request.GET.get("location", "")
    
    locations = Location.objects.all()
    
    # Initialize subcategories queryset
    subcategories = SubCategory.objects.none()
    
    # If a location is selected, filter subcategories
    if selected_location_id:
        subcategories = SubCategory.objects.filter(category__location_name__id=selected_location_id)


    
    if request.method == "POST":
        if "add_room" in request.POST:
            subcategory_id = request.POST.get("subcategory")
            location_id = request.POST.get("location")
            room_rent = request.POST.get("room_rent")
            room_details = request.POST.get("room_details")
            available_room = request.POST.get("available_room")
            room_images = request.FILES.getlist("room_images")

            subcategory = get_object_or_404(SubCategory, id=subcategory_id)
            location = get_object_or_404(Location, id=location_id)

            # Create the Room instance
            room = Room.objects.create(
                subcategory=subcategory,
                location=location,
                room_rent=room_rent,
                room_details=room_details,
                available_room=available_room,
            )

            # Save multiple images
            for image in room_images:
                RoomImage.objects.create(room=room, image=image)

            return redirect("room_rate")

    return render(
        request,
        "adminside/room_rate.html",
        {
            "locations": locations,
            "subcategories": subcategories,
            "selected_location_id": selected_location_id,
        },
    )