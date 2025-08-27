from django.db import models
from django.conf import settings

class Job(models.Model):
    recruiter = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="posted_jobs")
    title = models.CharField(max_length=160)
    description = models.TextField()
    company_name = models.CharField(max_length=255, null=True, blank=True)
    skills_required = models.TextField()  # "Python, Django, SQL"
    min_cgpa = models.DecimalField(max_digits=3, decimal_places=2, null=True, blank=True)
    location = models.CharField(max_length=120, blank=True)
    ctc = models.CharField(max_length=60, blank=True)
    deadline = models.DateTimeField()
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    eligibility_criteria = models.TextField(null=True, blank=True)

class Application(models.Model):
    PENDING, SHORTLISTED, REJECTED, SELECTED = "pending","shortlisted","rejected","selected"
    STATUS_CHOICES = [(PENDING,"Pending"),(SHORTLISTED,"Shortlisted"),(REJECTED,"Rejected"),(SELECTED,"Selected")]
    student = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="applications")
    job = models.ForeignKey(Job, on_delete=models.CASCADE, related_name="applications")
    cover_letter = models.TextField(blank=True)
    resume = models.FileField(upload_to="applications/resumes/", null=True, blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default=PENDING)
    applied_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("student","job")
