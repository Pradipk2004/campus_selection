# interviews/signals.py
from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Interview
from notifications.models import Notification
from analytics.models import InterviewPerformance


@receiver(post_save, sender=Interview)
def notify_interview(sender, instance, created, **kwargs):
    student = instance.application.student
    title = "Interview Scheduled" if created else "Interview Updated"
    body = f"{instance.application.job.title} at {instance.scheduled_at}"
    Notification.objects.create(
        user=student, title=title, body=body, url=f"/interviews/{instance.id}/"
    )


@receiver(post_save, sender=Interview)
def compute_performance(sender, instance, created, **kwargs):
    if instance.rating_by_recruiter:
        score = float(instance.rating_by_recruiter) * 20.0   # simple 0-100
        strengths = "Good communication" if instance.rating_by_recruiter >= 4 else ""
        improvements = "Revise data structures & system design basics." if instance.rating_by_recruiter <= 3 else ""
        InterviewPerformance.objects.update_or_create(
            interview=instance,
            defaults={
                "student": instance.application.student,
                "score": score,
                "strengths": strengths,
                "improvements": improvements,
            }
        )
