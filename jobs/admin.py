# jobs/admin.py
from django.contrib import admin
from .models import Job, Application

@admin.register(Job)
class JobAdmin(admin.ModelAdmin):
    list_display = ('title', 'recruiter', 'eligibility_criteria', 'location', 'created_at')
    list_filter = ('recruiter', 'location')
    search_fields = ('title', 'recruiter__user__username')

@admin.register(Application)
class ApplicationAdmin(admin.ModelAdmin):
    list_display = ('student', 'job', 'status', 'applied_at')
    list_filter = ('status',)
    search_fields = ('student__user__username', 'job__title')
