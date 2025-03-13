from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required, user_passes_test
from django.utils.timezone import now
from .models import DailyHomework, HomeworkTask, ChildProgress
from .forms import DailyHomeworkForm, HomeworkTaskFormSet
from rest_framework import generics, permissions
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes

from .serializers import DailyHomeworkSerializer

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
        homework_form = DailyHomeworkForm(request.POST)
        # Use a blank instance of DailyHomework so the formset can attach
        homework_instance = DailyHomework(teacher=request.user)
        task_formset = HomeworkTaskFormSet(request.POST, instance=homework_instance)

        if homework_form.is_valid() and task_formset.is_valid():
            # Save the DailyHomework
            daily_homework = homework_form.save(commit=False)
            daily_homework.teacher = request.user
            daily_homework.save()

            # Now save the tasks, linking them to the saved daily_homework
            task_formset.instance = daily_homework
            task_formset.save()

            return redirect("teacher_dashboard")
    else:
        # GET request: Display empty forms
        homework_form = DailyHomeworkForm()
        # Provide an empty DailyHomework object so the formset knows how to link tasks
        homework_instance = DailyHomework(teacher=request.user)
        task_formset = HomeworkTaskFormSet(instance=homework_instance)

    return render(request, "homework/create_homework.html", {
        "homework_form": homework_form,
        "task_formset": task_formset,
    })


@login_required
@user_passes_test(is_teacher)
def teacher_dashboard(request):
    # e.g., list all homework created by this teacher
    homeworks = DailyHomework.objects.filter(teacher=request.user).order_by('-date')
    return render(request, 'homework/teacher_dashboard.html', {'homeworks': homeworks})


#  Child: View & Complete Homework
@login_required
@user_passes_test(is_child)
def child_dashboard(request):
    child = request.user.child_profile  # Get child profile
   # today_homework = DailyHomework.objects.filter(date=now().date())
    today_homework = DailyHomework.objects.filter(date=now().date(),teacher=child.teacher)

    if request.method == "POST":
        task_id = request.POST.get("task_id")
        task = HomeworkTask.objects.get(id=task_id)

        # Prevent duplicate progress entries
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


# Parent: View Child Progress
@login_required
@user_passes_test(is_parent)
def parent_dashboard(request):
    children = request.user.children.all()  # Get linked children
    progress = ChildProgress.objects.filter(child__in=children)
    return render(request, "homework/parent_dashboard.html", {"progress": progress})


@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def create_daily_homework_api(request):
    serializer = DailyHomeworkSerializer(data=request.data)
    if serializer.is_valid():
        daily_hw = serializer.save(teacher=request.user)
        return Response({'success': True, 'id': daily_hw.id})
    return Response(serializer.errors, status=400)