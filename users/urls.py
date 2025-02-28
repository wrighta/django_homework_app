from django.urls import path
from . import views
from django.contrib.auth import views as auth_views  # Import Django's auth views

urlpatterns = [
    path('login/', auth_views.LoginView.as_view(), name='login'),  # Use built-in login view
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),  # Use built-in logout view
]
