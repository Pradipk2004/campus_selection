# accounts/forms.py
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model
from accounts.models import RecruiterProfile, StudentProfile
from .models import CustomUser 



class CustomUserRegisterForm(UserCreationForm):
    email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'placeholder': 'Email'
        })
    )

    role = forms.ChoiceField(
        choices=CustomUser.ROLE_CHOICES,  # FIXED (use CustomUser not User)
        required=True,
        widget=forms.Select(attrs={'class': 'form-select'})
    )

    class Meta:
        model = CustomUser   # FIXED
        fields = ['username', 'email', 'role', 'password1', 'password2']
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Username'}),
            'password1': forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Password'}),
            'password2': forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Confirm Password'}),
        }

    def clean_role(self):
        role = self.cleaned_data.get("role")
        if role not in dict(CustomUser.ROLE_CHOICES).keys():
            raise forms.ValidationError("Invalid role selected.")
        return role

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        user.role = self.cleaned_data['role']
        if commit:
            user.save()  #  triggers signal → creates profile
        return user


class StudentProfileForm(forms.ModelForm):
    YEAR_CHOICES = [
        (1, "1st Year"),
        (2, "2nd Year"),
        (3, "3rd Year"),
        (4, "4th Year"),
    ]

    year = forms.ChoiceField(
        choices=YEAR_CHOICES,
        required=False,
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    class Meta:
        model = StudentProfile
        fields = ["full_name", "phone", "branch", "year", "cgpa", "skills", "resume", "certifications"]
        widgets = {
            "full_name": forms.TextInput(attrs={"class": "form-control", "placeholder": "Full Name"}),
            "phone": forms.TextInput(attrs={"class": "form-control", "placeholder": "Phone"}),
            "branch": forms.TextInput(attrs={"class": "form-control", "placeholder": "Branch"}),
            "cgpa": forms.NumberInput(attrs={"class": "form-control", "step": "0.01"}),
            "skills": forms.Textarea(attrs={"class": "form-control", "placeholder": "Enter skills"}),
            "resume": forms.FileInput(attrs={"class": "form-control"}),
            "certifications": forms.FileInput(attrs={"class": "form-control"}),
        }


class RecruiterProfileForm(forms.ModelForm):
    class Meta:
        model = RecruiterProfile
        fields = ['company_name', 'contact_number']
        widgets = {
            "company_name": forms.TextInput(attrs={"class": "form-control", "placeholder": "Company Name"}),
            "contact_number": forms.TextInput(attrs={"class": "form-control", "placeholder": "Contact Number"}),
        }


class EditProfileForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'first_name', 'last_name']
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Username'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Email'}),
            'first_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'First Name'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Last Name'}),
        }
