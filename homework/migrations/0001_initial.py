# Generated by Django 5.1.5 on 2025-02-28 18:51

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('users', '__first__'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='DailyHomework',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField()),
                ('teacher', models.ForeignKey(limit_choices_to={'role': 'teacher'}, on_delete=django.db.models.deletion.CASCADE, related_name='homework', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='HomeworkTask',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('subject', models.CharField(max_length=100)),
                ('description', models.TextField()),
                ('daily_homework', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='tasks', to='homework.dailyhomework')),
            ],
        ),
        migrations.CreateModel(
            name='ChildProgress',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField()),
                ('completed', models.BooleanField(default=False)),
                ('child', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='users.child')),
                ('homework_task', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='homework.homeworktask')),
            ],
        ),
    ]
