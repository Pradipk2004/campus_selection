from django.db import models
from django.conf import settings
from jobs.models import Job
from accounts.models import CustomUser

class Conversation(models.Model):
    job = models.ForeignKey(Job, on_delete=models.CASCADE, related_name="conversations")
    student = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="student_conversations")
    recruiter = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="recruiter_conversations")
    created_at = models.DateTimeField(auto_now_add=True)


class ChatMessage(models.Model):
    SENDER_CHOICES = [
        ('student', 'Student'),
        ('recruiter', 'Recruiter'),
    ]
    sender = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='sent_messages')
    receiver = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='received_messages')
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    sender_type = models.CharField(max_length=20, choices=SENDER_CHOICES)

    def __str__(self):
        return f"{self.sender.username} -> {self.receiver.username}"

