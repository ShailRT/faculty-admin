from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser, ProgramOutcome

class CustomUserForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = UserCreationForm.Meta.fields + ('photo', 'college', 'department', 'email', 'contact_number', 'first_name', 'last_name')

class ProgramOutcomeForm(ModelForm):
    class Meta:
        model = ProgramOutcome
        fields = ['number', 'message', 'program']