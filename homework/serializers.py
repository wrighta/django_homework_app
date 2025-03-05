from rest_framework import serializers
from .models import DailyHomework, HomeworkTask

class DailyHomeworkSerializer(serializers.ModelSerializer):
    class Meta:
        model = DailyHomework
        fields = ['id', 'teacher', 'date']

    # Optional: make 'teacher' read-only if you always set it to request.user
    read_only_fields = ['teacher']
