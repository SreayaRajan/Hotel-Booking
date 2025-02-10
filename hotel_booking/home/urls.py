from django.urls import path
from .views import *
from . import views
# from .views import login_view


urlpatterns = [
    path('', views.index, name='index'), 
    path('register/', views.register, name='register'),
      path("login/", views.loginn, name="login"),
         path("sucess/", views.sucess, name="sucess"),
    
]
