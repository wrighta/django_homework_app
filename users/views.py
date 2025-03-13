from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required, user_passes_test
from rest_framework.decorators import api_view, permission_classes
from rest_framework import permissions, status
from rest_framework.response import Response
from django.contrib.auth import get_user_model
from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import AuthenticationForm
from .serializers import TeacherRegistrationSerializer
from django.views.decorators.csrf import csrf_exempt
from django.db import transaction
from .models import Child
from .serializers import ChildCreationSerializer

User = get_user_model()

########## USER LOGIN ###########
@csrf_exempt  # if you haven't set up proper CSRF for API endpoints
@api_view(['GET','POST'])
@permission_classes([permissions.AllowAny])
def user_login_view(request):
    """
    Log in a user (teacher, parent, child) with username/password.
    Return their role on success.
    """
    
    if request.method == 'GET':
        form = AuthenticationForm()
        return render(request, 'registration/login.html', {'form': form})
    
    elif request.method == 'POST':
        username = request.data.get('username')
        password = request.data.get('password')

        if not username or not password:
            return Response({'error': 'Username and password required.'},
                            status=status.HTTP_400_BAD_REQUEST)

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            # If teacher, go to teacher_dashboard; else to a different page
            if is_teacher(user):
                return redirect('teacher_dashboard')

        else:
            return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)



def is_teacher(user):
    return user.is_authenticated and user.role == "teacher"

def is_child(user):
    return user.is_authenticated and user.role == "child"

def is_parent(user):
    return user.is_authenticated and user.role == "parent"

@login_required
@user_passes_test(is_teacher)
def teacher_dashboard(request):
    return render(request, "homework/teacher_dashboard.html")

@login_required
@user_passes_test(is_child)
def child_dashboard(request):
    return render(request, "child_dashboard.html")

@login_required
@user_passes_test(is_parent)
def parent_dashboard(request):
    return render(request, "parent_dashboard.html")
# Create your views here.

####################################################
##############REACT API FUNCTIONS ##################
####################################################

@csrf_exempt  # if you haven't set up proper CSRF for API endpoints
@api_view(['POST'])
@permission_classes([permissions.AllowAny])
def create_child_view(request):
    # Hardcode the teacher ID
    teacher_id = 6  # Replace with the actual teacher ID you want to hardcode


    data = request.data

    child_username = data.get("child_username")
    child_password = data.get("child_password")
    selected_parent_id = data.get("selected_parent")
    new_parent_username = data.get("new_parent_username")
    new_parent_password = data.get("new_parent_password")

    # Validate child fields
    if not child_username or not child_password:
        return Response({"error": "Child username and password are required."},
                        status=status.HTTP_400_BAD_REQUEST)
    
    # 1) Determine the parent
    parent_user = None
    if selected_parent_id:
        # Link to existing parent
        try:
            parent_user = User.objects.get(id=selected_parent_id, role='parent')
        except User.DoesNotExist:
            return Response({"error": "Parent not found or invalid role."},
                            status=status.HTTP_400_BAD_REQUEST)
    else:
        # Possibly create a new parent
        if new_parent_username and new_parent_password:
            # Check if username is taken
            if User.objects.filter(username=new_parent_username).exists():
                return Response({"error": "Parent username is already in use."},
                                status=status.HTTP_400_BAD_REQUEST)
            # Create parent user
            parent_user = User.objects.create(
                username=new_parent_username,
                role='parent',
                password=new_parent_password
            )
        else:
            # No existing parent or new parent details provided
            return Response({"error": "Either select an existing parent or provide new parent credentials."},
                            status=status.HTTP_400_BAD_REQUEST)

    # 2) Create the child user
    if User.objects.filter(username=child_username).exists():
        return Response({"error": "Child username is already in use."},
                        status=status.HTTP_400_BAD_REQUEST)

    child_user = User.objects.create(
        username=child_username,
        role='child',
        password=child_password
    )

    # 3) Create a Child model record to link them
    Child.objects.create(
        child_user=child_user,
        teacher=teacher_id,  # Hardcoded teacher ID
        parent=parent_user   # whichever parent we determined
    )

    return Response({"message": "Child user created successfully."}, status=status.HTTP_201_CREATED)


###### GET EXISTING PARENTS #######
@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def existing_parents_view(request):
    """
    Fetch a list of existing parents.
    """
    parents = User.objects.filter(role='parent')
    parent_data = [{"id": parent.id, "username": parent.username} for parent in parents]
    return Response(parent_data, status=status.HTTP_200_OK)


######### REGISTER TEACHER ############
@api_view(['POST'])
@permission_classes([permissions.AllowAny])  # Anyone can register
def teacher_register_view(request):
    """
    Create a Teacher user, then automatically log them in using Django session.
    """
    serializer = TeacherRegistrationSerializer(data=request.data)
    if serializer.is_valid():
        user = serializer.save()  # Creates the teacher user (role=teacher)
        
        # Now automatically log them in with Django's session-based auth
        # For this to work, you must have 'SessionAuthentication' in DRF or
        # rely on standard Django's session middleware.
        
        # 1) We must authenticate with the new credentials:
        # Since the user was just created, we can re-check the request data:
        username = request.data.get('username')
        password = request.data.get('password')
        
        # Attempt to authenticate:
        user = authenticate(request, username=username, password=password)
        if user is not None:
            # 2) Log them in, attaching the session to this request
            login(request, user)
            return Response({"message": "Teacher registered and logged in."},
                            status=status.HTTP_201_CREATED)
        else:
            # This theoretically shouldn't fail unless the password hashing
            # logic didn't match. But just in case:
            return Response({"error": "Authentication failed after registration."},
                            status=status.HTTP_400_BAD_REQUEST)
    else:
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

