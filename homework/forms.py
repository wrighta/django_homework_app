from django import forms
from django.forms import inlineformset_factory
from .models import DailyHomework, HomeworkTask

class DailyHomeworkForm(forms.ModelForm):
    date = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date'}),
        required=True
    )
    class Meta:
        model = DailyHomework
        fields = ['date']

class HomeworkTaskForm(forms.ModelForm):
    class Meta:
        model = HomeworkTask
        fields = ['subject', 'description']

# Create an inline formset for HomeworkTask linked to DailyHomework:
HomeworkTaskFormSet = inlineformset_factory(
    DailyHomework,
    HomeworkTask,
    form=HomeworkTaskForm,
    extra=3,           # Number of extra blank forms to display
    can_delete=True    # Allow tasks to be deleted if needed
)

# class DailyHomeworkForm(forms.ModelForm):
#     class Meta:
#         model = DailyHomework
#         fields = ["date"]

# class HomeworkTaskForm(forms.ModelForm):
#     class Meta:
#         model = HomeworkTask
#         fields = ["daily_homework", "subject", "description"]
