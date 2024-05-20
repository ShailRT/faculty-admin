from django.db import models
from django.contrib.auth.models import AbstractUser
import uuid

department_choices = ( ('IT', 'IT' ), ('CS', 'CS'), ('AI/ML', 'AI/ML'), ('IOT', 'IOT'))
program_choices = ( ('B.Tech', 'B.Tech' ),)
college_choices = (('GNIOT','GNIOT'), ('GIMS', 'GIMS'))
request_choices = (('TABLE_EDIT_ACCESS','TABLE_EDIT_ACCESS'), ('USER_LOGIN_ACCESS', 'USER_LOGIN_ACCESS'))

class College(models.Model):
    uuid = models.UUIDField(default=uuid.uuid4, primary_key=True, editable=False)
    title = models.CharField(max_length=120)
    location = models.CharField(max_length=200)

    def __str__(self):
        return self.title
    
class Subject(models.Model):
    uuid = models.UUIDField(default=uuid.uuid4, primary_key=True, editable=False)
    title = models.CharField(max_length=120)
    code = models.CharField(max_length=10)
    program = models.CharField(max_length=120, blank=True, null=True)

    def __str__(self):
        return self.code

class FacultyInfo(models.Model):
    college_name = models.CharField(choices=college_choices ,max_length=120)
    department = models.CharField(choices=department_choices, max_length=20)
    college_id = models.CharField(max_length=20)
    college_email = models.EmailField()
    first_name = models.CharField(max_length=10)
    last_name = models.CharField(max_length=10)

    def __str__(self):
        return self.college_id
    
class CustomUser(AbstractUser):
    photo = models.ImageField(upload_to='faculty_profile')
    college = models.ForeignKey(College, on_delete=models.SET_NULL, null=True, blank=True)
    department = models.CharField(max_length=20, choices=department_choices, null=True, blank=True)
    contact_number = models.CharField(max_length=10, null=True, blank=True)
    subjects = models.ManyToManyField(Subject, blank=True)
    is_login_permitted = models.BooleanField(default=False)
    is_editing_table_permitted = models.BooleanField(default=False)
    is_sessional_table_editing_permitted = models.BooleanField(default=False)
    
    def __str__(self):
        return self.username

class AccessRequest(models.Model):
    uuid = models.UUIDField(default=uuid.uuid4, editable=False)
    message = models.CharField(max_length=20, choices=request_choices)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    is_reviewed = models.BooleanField(default=False)
    date_created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['is_reviewed', '-date_created']

    def __str__(self):
        return self.message

class CourseOutcome(models.Model):
    uuid = models.UUIDField(default=uuid.uuid4, editable=False)
    number = models.CharField(max_length=2)
    message = models.TextField()
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    program_outcome_priority = models.JSONField()
    program_educational_objective_priority = models.JSONField()
    program_specific_outcome_priority = models.JSONField()

    class Meta:
        ordering = ['number']

    def __str__(self):
        return f"CO{self.number} - {self.subject.title}"

        
    
class ProgramEducationalObjective(models.Model):
    uuid = models.UUIDField(default=uuid.uuid4, editable=False)
    number = models.IntegerField()
    message = models.TextField()
    program = models.CharField(max_length=120, choices=program_choices)
    department = models.CharField(max_length=20, choices=department_choices)

    class Meta:
        ordering = ['number']

    def __str__(self):
        return f"PEO{self.number} - {self.program}"

class ProgramSpecificOutcome(models.Model):
    uuid = models.UUIDField(default=uuid.uuid4, editable=False)
    number = models.IntegerField()
    message = models.TextField()
    program = models.CharField(max_length=120, choices=program_choices)
    department = models.CharField(max_length=20, choices=department_choices)

    class Meta:
        ordering = ['number']

    def __str__(self):
        return f"PSO{self.number} - {self.program}"
    
class ProgramOutcome(models.Model):
    uuid = models.UUIDField(default=uuid.uuid4, editable=False)
    number = models.IntegerField()
    message = models.TextField()
    program = models.CharField(max_length=120, choices=program_choices)

    class Meta:
        ordering = ['number']

    def __str__(self):
        return f"PO{self.number} - {self.program}"
    


    


