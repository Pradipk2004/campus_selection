from django.conf import settings
from django.db import models

class InterviewPerformance(models.Model):
    student = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="interview_performance")
    interview = models.OneToOneField("interviews.Interview", on_delete=models.CASCADE)
    score = models.FloatField(default=0.0)  # compute from rating + heuristics
    strengths = models.TextField(blank=True)
    improvements = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

