from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required, user_passes_test
from django.utils.timezone import now
from .models import DailyHomework, HomeworkTask, ChildProgress
from .forms import DailyHomeworkForm, HomeworkTaskForm


# ✅ Helper Functions
def is_teacher(user):
    """Check if the user is a teacher"""
    return user.is_authenticated and user.role == "teacher"

def is_child(user):
    """Check if the user is a child"""
    return user.is_authenticated and user.role == "child"

def is_parent(user):
    """Check if the user is a parent"""
    return user.is_authenticated and user.role == "parent"


# ✅ Teacher: Create Homework
@login_required
@user_passes_test(is_teacher)
def create_homework(request):
    if request.method == "POST":
        form = DailyHomeworkForm(request.POST)
        if form.is_valid():
            homework = form.save(commit=False)
            homework.teacher = request.user  # Assign logged-in teacher
            homework.save()
            return redirect("teacher_dashboard")
    else:
        form = DailyHomeworkForm()
    return render(request, "homework/create_homework.html", {"form": form})


# ✅ Child: View & Complete Homework
@login_required
@user_passes_test(is_child)
def child_dashboard(request):
    child = request.user.child_profile  # Get child profile
    today_homework = DailyHomework.objects.filter(date=now().date())

    if request.method == "POST":
        task_id = request.POST.get("task_id")
        task = HomeworkTask.objects.get(id=task_id)

        # ✅ Prevent duplicate progress entries
        progress, created = ChildProgress.objects.get_or_create(
            child=child, homework_task=task,
            defaults={"completed": True, "date": now().date()}
        )

        if not created:
            progress.completed = True  # Mark as completed
            progress.save()

    completed_tasks = ChildProgress.objects.filter(child=child)
    return render(request, "homework/child_dashboard.html", {
        "homework": today_homework,
        "completed_tasks": completed_tasks
    })


# ✅ Parent: View Child Progress
@login_required
@user_passes_test(is_parent)
def parent_dashboard(request):
    children = request.user.children.all()  # Get linked children
    progress = ChildProgress.objects.filter(child__in=children)
    return render(request, "homework/parent_dashboard.html", {"progress": progress})
