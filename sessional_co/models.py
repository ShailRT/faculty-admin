from django.db import models
from core.models import Subject, CustomUser
from exit_survey.models import SessionStudent
import uuid

semester_choices = (('1st', '1st'),('2nd', '2nd'),('3rd', '3rd'),('4th', '4th'),('5th', '5th'),('6th', '6th'),('7th', '7th'),('8th', '8th'))

class SessionalTable(models.Model):
    uuid = models.UUIDField(default=uuid.uuid4, editable=False)
    faculty = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True, blank=True)
    session = models.ForeignKey(SessionStudent, on_delete=models.CASCADE)
    semester = models.CharField(max_length=10, choices=semester_choices)
    subject = models.ForeignKey(Subject, null=True, blank=True, on_delete=models.SET_NULL)
    ct1 = models.JSONField(blank=True, null=True)
    ct2 = models.JSONField(blank=True, null=True)
    put = models.JSONField(blank=True, null=True)
    assignment_tutorial = models.JSONField(blank=True, null=True)
    max_marks = models.JSONField(blank=True, null=True)
    date_created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-date_created']

    def __str__(self):
        return f"{self.subject.code} {self.semester} [{self.session.session}] [{self.session.department}]"
    



    

