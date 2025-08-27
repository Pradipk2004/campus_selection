from django import forms
from .models import Application, Interview, Job

class JobApplicationForm(forms.ModelForm):
    class Meta:
        model = Application
        fields = ['resume']

class InterviewForm(forms.ModelForm):
    class Meta:
        model = Interview
        fields = ['date', 'mode']
