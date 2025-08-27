# interviews/views.py
from django.http import HttpResponseForbidden
from django.views.generic import ListView, DetailView
from django.contrib.auth.mixins import LoginRequiredMixin

from jobs.models import Application
from .models import Interview
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.mail import send_mail
from .forms import InterviewForm
from django.conf import settings
from django.db import IntegrityError
def notify_student(interview, message):
    """Send simple email notification to student."""
    student_email = interview.application.student.email
    subject = "Interview Update Notification"
    body = f"""
    Dear {interview.application.student.username},

    {message}

    Job: {interview.application.job.title}
    Scheduled At: {interview.scheduled_at}
    Meeting Link: {interview.meeting_link or 'N/A'}

    Regards,
    Campus Recruitment System
    """
    send_mail(subject, body, settings.DEFAULT_FROM_EMAIL, [student_email])




@login_required
def student_interviews(request):
    if request.user.role != "student":
        return render(request, "403.html", status=403)

    # Filter using the logged-in student (CustomUser)
    interviews = Interview.objects.filter(
        application__student=request.user
    ).order_by("scheduled_at")

    return render(request, "interviews/student_interviews.html", {"interviews": interviews})





@login_required
def cancel_interview(request, pk):
    interview = get_object_or_404(Interview, pk=pk, recruiter=request.user)

    if request.method == "POST":
        notify_student(interview, "Your interview has been cancelled.")
        interview.delete()
        messages.success(request, "Interview cancelled successfully!")
        return redirect("interviews:interviews")

    return render(request, "interviews/cancel_confirm.html", {"interview": interview})


class InterviewListView(LoginRequiredMixin, ListView):
    template_name = 'interviews/list.html'
    context_object_name = 'interviews'

    def get_queryset(self):
        return Interview.objects.filter(
            application__student=self.request.user
        ).order_by('scheduled_at')


class InterviewDetailView(LoginRequiredMixin, DetailView):
    model = Interview
    template_name = "interviews/detail.html"
