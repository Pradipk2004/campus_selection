from django.contrib import admin
from .models import Interview

@admin.register(Interview)
class InterviewAdmin(admin.ModelAdmin):
    list_display = ('get_job', 'get_student', 'recruiter', 'scheduled_at', 'status')

    def get_job(self, obj):
        return obj.application.job.title
    get_job.short_description = 'Job'

    def get_student(self, obj):
        return obj.application.student.username
    get_student.short_description = 'Student'
