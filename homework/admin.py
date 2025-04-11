from django.contrib import admin
from .models import HomeworkTask
from .models import DailyHomework


admin.site.register(DailyHomework)
admin.site.register(HomeworkTask)
admin.site.register()