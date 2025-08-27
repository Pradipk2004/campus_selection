from django.contrib.auth.models import AbstractUser
from django.db import models
from django.conf import settings


class CustomUser(AbstractUser):
    STUDENT = "student"
    RECRUITER = "recruiter"
    ADMIN = "admin"
    ROLE_CHOICES = [
        (STUDENT, "Student"),
        (RECRUITER, "Recruiter"),
        (ADMIN, "Admin"),
    ]
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default=ADMIN)  


class StudentProfile(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="student_profile"  # 👈 must match in signals
    )
    full_name = models.CharField(max_length=120, blank=True)
    phone = models.CharField(max_length=20, blank=True)
    branch = models.CharField(max_length=80, blank=True)
    year = models.IntegerField(null=True, blank=True)
    cgpa = models.DecimalField(max_digits=3, decimal_places=2, null=True, blank=True)
    skills = models.TextField(blank=True)  
    resume = models.FileField(upload_to='resumes/', null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True)
    certifications = models.FileField(upload_to="certifications/", blank=True, null=True) 
    
    def __str__(self):
        return self.user.username


class RecruiterProfile(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='recruiter_profile'  # 👈 must match in signals
    )
    company_name = models.CharField(max_length=255)
    contact_number = models.CharField(max_length=15, blank=True, null=True)
    bio = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.user.username} - {self.company_name}"



def resume_upload_path(instance, filename):
    return f"resumes/{instance.user_id}/{filename}"


def doc_upload_path(instance, filename):
    return f"docs/{instance.user_id}/{filename}"


class StudentDocument(models.Model):
    DOC_TYPES = [("resume", "Resume"), ("certificate", "Certificate"), ("other", "Other")]
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="documents")
    doc_type = models.CharField(max_length=20, choices=DOC_TYPES, default="other")
    file = models.FileField(upload_to=doc_upload_path)
    title = models.CharField(max_length=160, blank=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)


class ResumeAnalysis(models.Model):
    student = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="resume_analysis")
    skills_detected = models.JSONField(default=list)
    summary = models.TextField(blank=True)    # feedback
    updated_at = models.DateTimeField(auto_now=True)
