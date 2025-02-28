from django.urls import path
from . import views

urlpatterns = [
    path('create_homework/', views.create_homework, name='create_homework'),  # Teacher creates homework
    path('child_dashboard/', views.child_dashboard, name='child_dashboard'),  # Child's dashboard
    path('parent_dashboard/', views.parent_dashboard, name='parent_dashboard'),  # Parent's dashboard
]

