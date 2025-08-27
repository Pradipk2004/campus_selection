from rest_framework import viewsets, permissions
from .models import StudentDocument
from .serializers import StudentDocumentSerializer
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

class IsOwner(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj.user_id == request.user.id

class StudentDocumentViewSet(viewsets.ModelViewSet):
    serializer_class = StudentDocumentSerializer
    permission_classes = [permissions.IsAuthenticated, IsOwner]

    def get_queryset(self):
        return StudentDocument.objects.filter(user=self.request.user).order_by("-uploaded_at")

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
@api_view(["GET"])
@permission_classes([IsAuthenticated])
def my_resume_feedback(request):
    ra = getattr(request.user, "resume_analysis", None)
    if not ra:
        return Response({"status":"pending","message":"No analysis yet."})
    return Response({"skills_detected": ra.skills_detected, "summary": ra.summary, "updated_at": ra.updated_at})