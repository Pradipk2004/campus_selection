# core/admin.py
from django.contrib import admin
from django.urls import path
from django.template.response import TemplateResponse
from accounts.models import CustomUser
from jobs.models import Application
from jobs.models import Job
from interviews.models import Interview

class CustomAdminSite(admin.AdminSite):
    site_header = "Campus Selection System Admin"
    site_title = "Campus Admin"
    index_title = "Dashboard"

    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path('', self.admin_view(self.dashboard), name='index'),
        ]
        return custom_urls + urls

    def dashboard(self, request):
        total_students = CustomUser.objects.filter(role='student').count()
        total_recruiters = CustomUser.objects.filter(role='recruiter').count()
        total_jobs = Job.objects.count()
        total_applications = Application.objects.count()

        # Chart data: Applications by Job
        job_labels = list(Job.objects.values_list('title', flat=True))
        applications_data = [Application.objects.filter(job=job).count() for job in Job.objects.all()]

        # Chart data: Interviews scheduled by date
        interviews = Interview.objects.order_by('scheduled_at')
        interview_dates = [i.scheduled_at.strftime('%Y-%m-%d') for i in interviews]
        interview_counts = [interview_dates.count(date) for date in interview_dates]

        context = dict(
            self.each_context(request),
            total_students=total_students,
            total_recruiters=total_recruiters,
            total_jobs=total_jobs,
            total_applications=total_applications,
            job_labels=job_labels,
            applications_data=applications_data,
            interview_dates=interview_dates,
            interview_counts=interview_counts,
        )
        return TemplateResponse(request, "admin/index.html", context)


# Instantiate custom admin
custom_admin_site = CustomAdminSite(name='custom_admin')
