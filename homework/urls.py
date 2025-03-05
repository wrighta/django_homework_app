from django.urls import path
from . import views


urlpatterns = [
    path('api/create-daily-homework/', views.create_daily_homework_api, name='create-daily-homework-api'),
    path('create_homework/', views.create_homework, name='create_homework'),  # Teacher creates homework
    path('child_dashboard/', views.child_dashboard, name='child_dashboard'),  # Child's dashboard
    path('parent_dashboard/', views.parent_dashboard, name='parent_dashboard'),  # Parent's dashboard
]

