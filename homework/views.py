from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required, user_passes_test
from django.utils.timezone import now
from .models import DailyHomework, HomeworkTask, ChildProgress
from .forms import DailyHomeworkForm, HomeworkTaskFormSet, ChildCreationForm

from rest_framework import generics, permissions
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes

from .serializers import DailyHomeworkSerializer

# Helper Functions
def is_teacher(user):
    """Check if the user is a teacher"""
    return user.is_authenticated and user.role == "teacher"

def is_child(user):
    """Check if the user is a child"""
    return user.is_authenticated and user.role == "child"

def is_parent(user):
    """Check if the user is a parent"""
    return user.is_authenticated and user.role == "parent"

######################TEACHER FUNCTIONALITY ##########################

# Teacher: Create Homework
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

# homework/views.py

from django.shortcuts import render, redirect
from django.contrib.auth import get_user_model
from django.contrib.auth import login
from .forms import ChildCreationForm
from .models import Child

User = get_user_model()

def create_child_view(request):
    if request.method == 'POST':
        form = ChildCreationForm(request.POST)
        if form.is_valid():
            # 1) Create the User with role='child'
            username = form.cleaned_data['username']
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']

            child_user = User.objects.create_user(
                username=username,
                password=password,
                first_name=first_name,
                last_name=last_name,
                email=email
            )
            child_user.role = 'child'
            child_user.save()

            # 2) Create the Child record, linking the teacher to this user
            Child.objects.create(
                child_user=child_user,
                teacher=request.user,
                # parent stays None if you want to skip it
            )

            # Optionally, log the child in or just redirect
            # login(request, child_user)  # Usually not needed here
            return redirect('teacher_dashboard')  # or some "success" page
    else:
        form = ChildCreationForm()

    return render(request, 'homework/create_child.html', {'form': form})

######################CHILD FUNCTIONALITY ##########################

# #  Child: View & Complete Homework
# @login_required
# @user_passes_test(is_child)
# def child_dashboard(request):
#     child = request.user.child_profile  # Get child profile
#    # today_homework = DailyHomework.objects.filter(date=now().date())
#     today_homework = DailyHomework.objects.filter(date=now().date(),teacher=child.teacher)

#     if request.method == "POST":
#         task_id = request.POST.get("task_id")
#         task = HomeworkTask.objects.get(id=task_id)

#         # Prevent duplicate progress entries
#         progress, created = ChildProgress.objects.get_or_create(
#             child=child, homework_task=task,
#             defaults={"completed": True, "date": now().date()}
#         )

#         if not created:
#             progress.completed = True  # Mark as completed
#             progress.save()

#     completed_tasks = ChildProgress.objects.filter(child=child)
#     return render(request, "homework/child_dashboard.html", {
#         "homework": today_homework,
#         "completed_tasks": completed_tasks
#     })

# homework/views.py

from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from datetime import date
from .models import Child, DailyHomework, HomeworkTask, ChildProgress

@login_required
def child_dashboard(request):
    # 1) Identify the Child object for the logged-in user.
    #    (Assuming only users with role='child' can access this view.)
    try:
        child = Child.objects.get(child_user=request.user)
    except Child.DoesNotExist:
        # Handle the case if they're not a child or no Child record found
        # Perhaps redirect or raise a 404
        return redirect('home')  # or some other page

    # 2) Find the teacher’s most recent DailyHomework (up to today).
    #    teacher = child.teacher
    #    daily_homework = teacher's daily homework with date <= today's date
    today = date.today()
    daily_homework = (DailyHomework.objects
                      .filter(teacher=child.teacher, date__lte=today)
                      .order_by('-date')
                      .first())
    
    # Prepare placeholders for the "prev" and "next" date logic (not yet implemented).
    prev_url = '#'  # later you can generate a real URL
    next_url = '#'
    
    # 3) If there's no daily_homework found, we’ll just display a message.
    if not daily_homework:
        context = {
            'daily_homework': None,
            'prev_url': prev_url,
            'next_url': next_url
        }
        return render(request, 'homework/child_dashboard.html', context)
    
    # 4) Get tasks for that homework
    tasks = HomeworkTask.objects.filter(daily_homework=daily_homework)
    
    if request.method == 'POST':
        # We have checkboxes named "completed_tasks" with values = task.id
        completed_task_ids = request.POST.getlist('completed_tasks')

        # For each task in the daily homework:
        for task in tasks:
            # Either update or create the ChildProgress entry
            progress, created = ChildProgress.objects.get_or_create(
                child=child,
                homework_task=task,
                date=daily_homework.date,
                defaults={'completed': False}
            )
            # If the task’s ID is in the submitted list, mark it as completed,
            # otherwise mark it as not completed
            progress.completed = (str(task.id) in completed_task_ids)
            progress.save()
        
        # Optional: If all tasks are completed, redirect to "game page"
        if len(completed_task_ids) == len(tasks):
            return redirect('child_game_page')  # define this URL/view as needed
        
        # Else re-render the dashboard
        return redirect('child_dashboard')

    # 5) On GET, build a progress_list for the template
    progress_list = []
    for task in tasks:
        # Find an existing progress record if any
        progress = ChildProgress.objects.filter(
            child=child,
            homework_task=task,
            date=daily_homework.date
        ).first()
        progress_list.append({
            'task': task,
            'completed': progress.completed if progress else False
        })
    
    context = {
        'daily_homework': daily_homework,
        'progress_list': progress_list,
        'prev_url': prev_url,
        'next_url': next_url
    }
    return render(request, 'homework/child_dashboard.html', context)



######################PARENT FUNCTIONALITY ##########################
# Parent: View Child Progress
@login_required
@user_passes_test(is_parent)
def parent_dashboard(request):
    children = request.user.children.all()  # Get linked children
    progress = ChildProgress.objects.filter(child__in=children)
    return render(request, "homework/parent_dashboard.html", {"progress": progress})



######################REACT API FUNCTIONALITY ##########################

@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def create_daily_homework_api(request):
    serializer = DailyHomeworkSerializer(data=request.data)
    if serializer.is_valid():
        daily_hw = serializer.save(teacher=request.user)
        return Response({'success': True, 'id': daily_hw.id})
    return Response(serializer.errors, status=400)

