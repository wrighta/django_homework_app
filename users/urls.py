from django.urls import path
from . import views
from django.contrib.auth import views as auth_views  # Import Django's auth views

urlpatterns = [
    
    path('api/register-teacher/', views.teacher_register_view, name='register-teacher'),
    path('api/create-child/', views.create_child_view, name='create-child'),
    path('api/existing-parents/', views.existing_parents_view, name='existing-parents'),
    path('api/login/', views.user_login_view, name='login-api'),
    
    path('api/existing-parents/', views.existing_parents_view, name='existing-parents'),
    path('api/create-child/', views.create_child_view, name='create-child'),
    #not sure I use these.
    path('login/', auth_views.LoginView.as_view(), name='login'),  # Use built-in login view
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),  # Use built-in logout view
]
