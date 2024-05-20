from django.db import models
from core.models import Subject, CustomUser
import uuid

department_choices = ( ('IT', 'IT' ), ('CS', 'CS'), ('AI/ML', 'AI/ML'), ('IOT', 'IOT'))


class StudentInfo(models.Model):
    university_roll_no = models.CharField(max_length=120, unique=True)
    first_name = models.CharField(max_length=120)
    last_name = models.CharField(max_length=120)
    co_response = models.JSONField(blank=True, null=True)

    def __str__(self):
        return self.university_roll_no
    

class SessionStudent(models.Model):
    uuid = models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True)
    faculty = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    session = models.CharField(max_length=10)
    department = models.CharField(choices=department_choices, max_length=10)
    program = models.CharField(max_length=120)
    students = models.ManyToManyField(StudentInfo)
    year = models.CharField(max_length=1)
    
    def __str__(self):
        return f'{self.session}-{self.department}'


class ExitSurvey(models.Model):
    session = models.ForeignKey(SessionStudent, on_delete=models.CASCADE)
    semester = models.CharField(max_length=5)
    subject = models.ForeignKey(Subject, on_delete=models.SET_NULL, blank=True, null=True)
    department = models.CharField(max_length=10, choices=department_choices)
    slug = models.SlugField()
    faculty = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True, blank=True)
    link_active = models.BooleanField(default=True)

    def __str__(self) -> str:
        return self.session.session
    