from django.db import models
from django.utils import timezone
from jobs.models import Application
from accounts.models import CustomUser

class Interview(models.Model):
    STATUS_CHOICES = [
        ('Upcoming', 'Upcoming'),
        ('Completed', 'Completed'),
        ('Cancelled', 'Cancelled'),
    ]
    MODE_CHOICES = [
        ("Online", "Online"),
        ("Offline", "Offline"),
        ("Zoom", "Zoom"),
        ("Google Meet", "Google Meet"),
    ]

    application = models.OneToOneField(
        Application, on_delete=models.CASCADE, related_name='interview'
    )
    recruiter = models.ForeignKey(
        CustomUser, on_delete=models.CASCADE, null=True, blank=True,
        related_name='scheduled_interviews'
    )
    scheduled_at = models.DateTimeField(default=timezone.now)
    meeting_link = models.URLField(blank=True, null=True)
    mode = models.CharField(max_length=50, choices=MODE_CHOICES, default='Online')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Upcoming')
    feedback = models.TextField(blank=True, null=True)
    rating_by_recruiter = models.PositiveIntegerField(blank=True, null=True)

    def __str__(self):
        return f"Interview: {self.application.student.username} - {self.application.job.title}"
