from django import forms
from .models import Interview

class InterviewForm(forms.ModelForm):
    class Meta:
        model = Interview
        fields = ["scheduled_at", "mode", "status", "meeting_link", "feedback"]
        widgets = {
            "scheduled_at": forms.DateTimeInput(
                attrs={"type": "datetime-local", "class": "form-control"}
            ),
            "mode": forms.Select(attrs={"class": "form-select"}),
            "status": forms.Select(attrs={"class": "form-select"}),
            "feedback": forms.Textarea(attrs={"class": "form-control", "rows": 3}),
        }
