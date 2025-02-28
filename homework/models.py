from django.db import models
from users.models import User, Child

class DailyHomework(models.Model):
    teacher = models.ForeignKey(User, on_delete=models.CASCADE, related_name="homework", limit_choices_to={'role': 'teacher'})
    date = models.DateField()

    def __str__(self):
        return f"{self.teacher.username} - {self.date}"

class HomeworkTask(models.Model):
    daily_homework = models.ForeignKey(DailyHomework, on_delete=models.CASCADE, related_name="tasks")
    subject = models.CharField(max_length=100)
    description = models.TextField()

    def __str__(self):
        return f"{self.subject}: {self.description}"

class ChildProgress(models.Model):
    child = models.ForeignKey(Child, on_delete=models.CASCADE)
    homework_task = models.ForeignKey(HomeworkTask, on_delete=models.CASCADE)
    date = models.DateField()
    completed = models.BooleanField(default=False)

    def __str__(self):
        status = "Completed" if self.completed else "Not Completed"
        return f"{self.child.user.username} - {self.homework_task.subject} ({status})"
