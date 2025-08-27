from rest_framework import viewsets, mixins, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Job, Application
from .serializers import JobSerializer, ApplicationSerializer

class JobViewSet(mixins.ListModelMixin, mixins.RetrieveModelMixin, viewsets.GenericViewSet):
    queryset = Job.objects.filter(is_active=True).order_by("-created_at")
    serializer_class = JobSerializer
    permission_classes = [permissions.AllowAny]

    def get_queryset(self):
        qs = super().get_queryset()
        q = self.request.query_params.get("q")
        skills = self.request.query_params.get("skills")
        location = self.request.query_params.get("location")
        if q: qs = qs.filter(title__icontains=q) | qs.filter(description__icontains=q)
        if skills: qs = qs.filter(skills_required__icontains=skills)
        if location: qs = qs.filter(location__icontains=location)
        return qs

class ApplicationViewSet(viewsets.ModelViewSet):
    serializer_class = ApplicationSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        # student sees their applications only
        return Application.objects.filter(student=self.request.user).select_related("job").order_by("-applied_at")

    def perform_create(self, serializer):
        serializer.save(student=self.request.user)
