from django import forms
from .models import DailyHomework, HomeworkTask

class DailyHomeworkForm(forms.ModelForm):
    class Meta:
        model = DailyHomework
        fields = ["date"]

class HomeworkTaskForm(forms.ModelForm):
    class Meta:
        model = HomeworkTask
        fields = ["daily_homework", "subject", "description"]
