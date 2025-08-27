from rest_framework import serializers
from .models import StudentDocument
from .models import StudentProfile

class StudentDocumentSerializer(serializers.ModelSerializer):
    class Meta:
        model = StudentDocument
        fields = ["id","doc_type","title","file","uploaded_at"]

class StudentProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = StudentProfile
        fields = ["full_name","phone","branch","year","cgpa","skills","resume","updated_at"]
