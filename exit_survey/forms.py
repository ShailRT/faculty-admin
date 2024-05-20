from django import forms
from .models import SessionStudent, StudentInfo, ExitSurvey
from django.utils.text import slugify
from core.models import CourseOutcome

class SurveyForm(forms.Form):
    first_name = forms.CharField(max_length=120)
    last_name = forms.CharField(max_length=120)
    uni_roll_no = forms.CharField(max_length=120)
    
class SessionStudentCreateForm(forms.ModelForm):
    class Meta:
        model = SessionStudent
        fields = ['session', 'department', 'program', 'year']
        
class CreateStudentInfoForm(forms.ModelForm):
    class Meta:
        model = StudentInfo
        fields = ['university_roll_no', 'first_name', 'last_name']
        

class ExitSurveyCreateForm(forms.ModelForm):
    class Meta:
        model = ExitSurvey
        fields = ['session', 'semester', 'department', 'subject']
        
    def save(self, commit=True):
        instance = super().save(commit=False)
        instance.slug = slugify(f'{self.cleaned_data['semester']}-{self.cleaned_data['department']}-{self.cleaned_data['subject']}')
        if commit:
            instance.save()
        return instance 
    
        