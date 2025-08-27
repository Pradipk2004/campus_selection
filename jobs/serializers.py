from rest_framework import serializers
from .models import Job, Application

class JobSerializer(serializers.ModelSerializer):
    class Meta:
        model = Job
        fields = ["id","title","description","skills_required","min_cgpa","location","ctc","deadline","is_active","created_at"]

class ApplicationSerializer(serializers.ModelSerializer):
    job_title = serializers.ReadOnlyField(source="job.title")
    class Meta:
        model = Application
        fields = ["id","job","job_title","cover_letter","resume","status","applied_at"]
        read_only_fields = ["status","applied_at"]
