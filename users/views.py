from django.shortcuts import render
from django.contrib.auth.decorators import login_required, user_passes_test

def is_teacher(user):
    return user.is_authenticated and user.role == "teacher"

def is_child(user):
    return user.is_authenticated and user.role == "child"

def is_parent(user):
    return user.is_authenticated and user.role == "parent"

@login_required
@user_passes_test(is_teacher)
def teacher_dashboard(request):
    return render(request, "teacher_dashboard.html")

@login_required
@user_passes_test(is_child)
def child_dashboard(request):
    return render(request, "child_dashboard.html")

@login_required
@user_passes_test(is_parent)
def parent_dashboard(request):
    return render(request, "parent_dashboard.html")
# Create your views here.
