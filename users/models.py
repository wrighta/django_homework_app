from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    ROLE_CHOICES = [
        ('teacher', 'Teacher'),
        ('parent', 'Parent'),
        ('child', 'Child'),
    ]
    role = models.CharField(max_length=10, choices=ROLE_CHOICES)

class Child(models.Model):
    child_user = models.OneToOneField(User,on_delete=models.CASCADE,related_name="child_profile")
    #user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="child_profile")
    teacher = models.ForeignKey(User, on_delete=models.CASCADE, related_name="students", limit_choices_to={'role': 'teacher'})
    parent = models.ForeignKey(User, on_delete=models.CASCADE, related_name="children", limit_choices_to={'role': 'parent'})
