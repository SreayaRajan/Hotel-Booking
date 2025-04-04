from django.urls import path
from . import views
from .views import booking_success


urlpatterns = [
    path('', views.index, name='index'), 
    path("register/", views.register, name="register"),
    path("login/", views.loginn, name="login"),
    path('logout/', views.user_logout, name='logout'),
    path("room/",views.room,name="room"),
    path('room_detail/<int:room_id>/', views.room_detail, name='room_detail'),
    path('booking/<int:room_id>/',views.booking_page, name='booking_page'),
    path('book/<int:room_id>/', views.book_room, name='book_room'),
    path('booking-success/<uuid:booking_id>/', booking_success, name='booking_success'),

    path("contact/",views.contact,name="contact"),
    path("service/",views.service,name="service"),
    path("team/",views.team,name="team"),
    path("testmonial/",views.testmonial,name="testmonial"),
    path("about/",views.about,name="about"),
    
#ADMIN SIDE
 path('index1', views.index1, name='index1'), 
 path('admin_login/', views.admin_login, name='admin_login'),
 path("admin_logout/", views.admin_logout, name="admin_logout"),
 path('dashboard/', views.dashboard, name='dashboard'),
path("location/", views.manage_location, name="manage_location"),
path("category/", views.manage_category, name="manage_category"),
path('subcategory/<int:category_id>/', views.manage_subcategory, name='manage_subcategory'),

path("room_rate/", views.manage_room, name="room_rate"),
path("room_details/", views.room_details, name="room_details"),


 
]
