from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from jobs.models import Application
from interviews.models import Interview

@api_view(["GET"])
@permission_classes([IsAuthenticated])
def my_overview(request):
    apps = Application.objects.filter(student=request.user).select_related("job").order_by("-applied_at")[:10]
    interviews = Interview.objects.filter(application__student=request.user).select_related("application__job").order_by("scheduled_at")[:10]
    return Response({
        "applications":[{"id":a.id,"job":a.job.title,"status":a.status,"applied_at":a.applied_at} for a in apps],
        "interviews":[{"id":iv.id,"job":iv.application.job.title,"when":iv.scheduled_at,"status":iv.status} for iv in interviews],
        "notifications_unread": request.user.notifications.filter(is_read=False).count(),
    })

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
