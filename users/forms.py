from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User

class TeacherRegistrationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'password1', 'password2']
        help_texts = {
                    'username': '',  # ← removes "Required. 150 characters..." bit
                    'password1': '',
                    'password2': '',
                }
        
    def save(self, commit=True):
        user = super().save(commit=False)
        user.role = 'teacher'
        user.is_staff = True  # Optional: gives admin access if needed
        if commit:
            user.save()
        return user