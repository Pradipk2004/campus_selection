from django import forms
from jobs.models import Job
from interviews.models import Interview

class JobForm(forms.ModelForm):
    class Meta:
        model = Job
        fields = ['title', 'company_name', 'description', 'eligibility_criteria', 'ctc', 'deadline']
        widgets = {
            'title': forms.TextInput(attrs={'class':'form-control'}),
            'description': forms.Textarea(attrs={'class':'form-control'}),
            'eligibility_criteria': forms.Textarea(attrs={'class':'form-control'}),
            'ctc': forms.TextInput(attrs={'class':'form-control'}),
            'deadline': forms.DateInput(attrs={'class':'form-control', 'type':'date'}),
        }

class JobCreateForm(forms.ModelForm):
    class Meta:
        model = Job
        fields = ['title', 'description', 'deadline']