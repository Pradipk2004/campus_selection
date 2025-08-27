from rest_framework.routers import DefaultRouter
from jobs.api import ApplicationViewSet, JobViewSet

router = DefaultRouter()
router.register(r"jobs", JobViewSet, basename="jobs")
router.register(r"me/applications", ApplicationViewSet, basename="me-applications")

urlpatterns = router.urls
