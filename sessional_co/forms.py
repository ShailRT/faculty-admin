from django import forms
from .models import SessionalTable

class SessionalTableCreateForm(forms.ModelForm):
    class Meta:
        model = SessionalTable
        fields = ['session', 'semester', 'subject']
    