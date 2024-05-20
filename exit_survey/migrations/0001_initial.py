# Generated by Django 4.2.7 on 2024-05-15 10:41

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('core', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='StudentInfo',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('university_roll_no', models.CharField(max_length=120, unique=True)),
                ('first_name', models.CharField(max_length=120)),
                ('last_name', models.CharField(max_length=120)),
                ('co_response', models.JSONField(blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='SessionStudent',
            fields=[
                ('uuid', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('session', models.CharField(max_length=10)),
                ('department', models.CharField(choices=[('IT', 'IT'), ('CS', 'CS'), ('AI/ML', 'AI/ML'), ('IOT', 'IOT')], max_length=10)),
                ('program', models.CharField(max_length=120)),
                ('year', models.CharField(max_length=1)),
                ('faculty', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('students', models.ManyToManyField(to='exit_survey.studentinfo')),
            ],
        ),
        migrations.CreateModel(
            name='ExitSurvey',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('semester', models.CharField(max_length=5)),
                ('department', models.CharField(choices=[('IT', 'IT'), ('CS', 'CS'), ('AI/ML', 'AI/ML'), ('IOT', 'IOT')], max_length=10)),
                ('slug', models.SlugField()),
                ('link_active', models.BooleanField(default=True)),
                ('faculty', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
                ('session', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='exit_survey.sessionstudent')),
                ('students', models.ManyToManyField(to='exit_survey.studentinfo')),
                ('subject', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='core.subject')),
            ],
        ),
    ]