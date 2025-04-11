from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.utils.timezone import now
from .models import DailyHomework, HomeworkTask, Child, ChildProgress
from .forms import DailyHomeworkForm, HomeworkTaskFormSet, ChildCreationForm
from django.contrib.auth import get_user_model
from django.contrib.auth import login
from django.urls import reverse
from datetime import date
import requests

from rest_framework import generics, permissions
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes

from .serializers import DailyHomeworkSerializer

User = get_user_model()

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




def homework_detail(request, pk):
    homework = get_object_or_404(DailyHomework, pk=pk)
    tasks = homework.tasks.all()  # Adjust if your model relation is different
    return render(request, 'homework/homework_detail.html', {'homework': homework, 'tasks': tasks})



######################CHILD FUNCTIONALITY ##########################

# loads child game page - this page displays all the pokemon cards from an external API
def child_game_page(request):
    return render(request, 'homework/child_game_page.html')

# When a child clicks a pokemon on the game page, it calls this function
# this function then gets the details of that pokemon from the external API 
# and passes it to the pokemon_detial
def pokemon_detail(request, pokemon_id):
    response = requests.get(f'https://pokeapi.co/api/v2/pokemon/{pokemon_id}/')
    if response.status_code == 200:
        pokemon_data = response.json()
    else:
        pokemon_data = None

    return render(request, 'homework/pokemon_detail.html', {
        'pokemon': pokemon_data
    })

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


@login_required
def child_dashboard(request, hw_id=None):
    # 1) Identify the Child object
    try:
        child = Child.objects.get(child_user=request.user)
    except Child.DoesNotExist:
        return redirect('home')  # or raise 404

    # 2) Determine which DailyHomework we’re showing
    #    If 'hw_id' is given, use that; otherwise load the latest available for this teacher up to (and including) today.
    teacher = child.teacher
    
    if hw_id:
        daily_homework = get_object_or_404(DailyHomework, pk=hw_id, teacher=teacher)
    else:
        # No hw_id => show the latest daily homework up to today's date
        daily_homework = (
            DailyHomework.objects
            .filter(teacher=teacher, date__lte=date.today())
            .order_by('-date')
            .first()
        )

    if not daily_homework:
        # No homework found => pass None to the template
        context = {
            'daily_homework': None,
            'prev_url': '#',
            'next_url': '#',
        }
        return render(request, 'homework/child_dashboard.html', context)

    # 3) Figure out “previous” and “next” homework
    #    “previous” => the DailyHomework with a date less than the current one, ordered descending, pick first.
    previous_hw = (
        DailyHomework.objects
        .filter(teacher=teacher, date__lt=daily_homework.date)
        .order_by('-date')
        .first()
    )
    next_hw = (
        DailyHomework.objects
        .filter(teacher=teacher, date__gt=daily_homework.date)
        .order_by('date')
        .first()
    )

    # Build the URLs for the template
    if previous_hw:
        prev_url = reverse('child_dashboard', kwargs={'hw_id': previous_hw.id})
    else:
        prev_url = '#'
    if next_hw:
        next_url = reverse('child_dashboard', kwargs={'hw_id': next_hw.id})
    else:
        next_url = '#'

    # 4) Now handle tasks for the chosen daily_homework
    tasks = HomeworkTask.objects.filter(daily_homework=daily_homework)

    if request.method == 'POST':
        # gather ticked checkboxes
        completed_task_ids = request.POST.getlist('completed_tasks')
        
        for task in tasks:
            progress, created = ChildProgress.objects.get_or_create(
                child=child,
                homework_task=task,
                date=daily_homework.date,
                defaults={'completed': False}
            )
            # Mark completed if the child ticked the box
            progress.completed = str(task.id) in completed_task_ids
            progress.save()

        # Check if all tasks are completed
        if len(completed_task_ids) == len(tasks):
            return redirect('child_game_page')

        # If not all completed, stay on the same homework date
        return redirect('child_dashboard', hw_id=daily_homework.id)

    # 5) On GET, build progress_list
    progress_list = []
    for task in tasks:
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
        'next_url': next_url,
    }
    return render(request, 'homework/child_dashboard.html', context)

# Load the game page. 
@login_required
def child_game_page(request):
    return render(request, "homework/child_game_page.html")


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

