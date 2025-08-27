from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from analytics.models import InterviewPerformance
from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import View
from jobs.models import Application, Job
from accounts.models import RecruiterProfile
from interviews.models import Interview

# Student analytics
class StudentAnalyticsView(LoginRequiredMixin, View):
    def get(self, request):
        apps_count = Application.objects.filter(student=request.user).count()
        interviews_count = Interview.objects.filter(application__student=request.user).count()
        jobs_applied = Application.objects.filter(student=request.user).select_related('job')
        context = {
            "apps_count": apps_count,
            "interviews_count": interviews_count,
            "jobs_applied": jobs_applied
        }
        return render(request, "analytics/student_analytics.html", context)

# Recruiter analytics
class RecruiterAnalyticsView(LoginRequiredMixin, View):
    def get(self, request):
        jobs_count = Job.objects.filter(recruiter=request.user.recruiter_profile).count()
        apps_count = Application.objects.filter(job__recruiter=request.user.recruiter_profile).count()
        interviews_count = Interview.objects.filter(recruiter=request.user).count()
        context = {
            "jobs_count": jobs_count,
            "apps_count": apps_count,
            "interviews_count": interviews_count
        }
        return render(request, "analytics/recruiter_analytics.html", context)

@api_view(["GET"])
@permission_classes([IsAuthenticated])
def my_performance(request):
    perf = request.user.interview_performance.select_related("interview__application__job").order_by("-created_at")[:10]
    data = [{
        "job": p.interview.application.job.title,
        "score": p.score,
        "strengths": p.strengths,
        "improvements": p.improvements,
        "when": p.created_at
    } for p in perf]
    return Response(data)
