from django.shortcuts import get_object_or_404, redirect
from django.views.generic import ListView, DetailView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from .models import Job, Application


class JobApplicationMixin:
    """Mixin to handle job application submission."""

    def handle_job_application(self, request, job):
        """Reusable logic for job application submission."""
        resume = request.FILES.get('resume')
        cover_letter = request.POST.get('cover_letter', '')

        # Validation
        if not resume:
            messages.error(request, "Please upload a resume.")
            return False

        # Duplicate check
        if Application.objects.filter(student=request.user, job=job).exists():
            messages.warning(request, "You have already applied for this job.")
            return False

        # Create application
        Application.objects.create(
            student=request.user,
            job=job,
            resume=resume,
            cover_letter=cover_letter
        )

        messages.success(request, f"Application submitted successfully for {job.title}!")
        return True


class JobListView(LoginRequiredMixin, JobApplicationMixin, ListView):
    model = Job
    template_name = "jobs/jobs_list.html"
    context_object_name = "jobs"

    def post(self, request, *args, **kwargs):
        job_id = request.POST.get('job_id')
        job = get_object_or_404(Job, id=job_id)
        self.handle_job_application(request, job)
        return redirect(request.path)  # reload page safely


class JobDetailView(LoginRequiredMixin, JobApplicationMixin, DetailView):
    model = Job
    template_name = "jobs/job_detail.html"
    context_object_name = "job"

    def post(self, request, *args, **kwargs):
        job = self.get_object()  # current Job instance
        self.handle_job_application(request, job)
        return redirect(request.path)  # reload page safely

class StudentApplicationsView(LoginRequiredMixin, ListView):
    model = Application
    template_name = 'jobs/applications.html'
    context_object_name = 'applications'

    def get_queryset(self):
        return Application.objects.filter(student=self.request.user).order_by('-applied_at')
