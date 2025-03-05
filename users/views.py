from django.shortcuts import render
from django.contrib.auth.decorators import login_required, user_passes_test
from rest_framework.decorators import api_view, permission_classes
from rest_framework import permissions, status
from rest_framework.response import Response
from django.contrib.auth import get_user_model
from django.contrib.auth import authenticate, login
from .serializers import TeacherRegistrationSerializer


from .models import Child
from .serializers import ChildCreationSerializer

User = get_user_model()

@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def create_child_view(request):
    """
    Create a child user and link them to the logged-in teacher and a parent.
    """
    serializer = ChildCreationSerializer(data=request.data, context={'request': request})
    if serializer.is_valid():
        serializer.save()
        return Response({"message": "Child user created successfully."}, status=status.HTTP_201_CREATED)
    else:
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def existing_parents_view(request):
    """
    Fetch a list of existing parents.
    """
    parents = User.objects.filter(role='parent')
    parent_data = [{"id": parent.id, "username": parent.username} for parent in parents]
    return Response(parent_data, status=status.HTTP_200_OK)

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
