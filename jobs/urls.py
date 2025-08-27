from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import JobListView, JobDetailView, StudentApplicationsView
from . import api

app_name = "jobs"

router = DefaultRouter()
router.register("jobs", api.JobViewSet, basename="jobs")
router.register("me/applications", api.ApplicationViewSet, basename="applications")

urlpatterns = [
    path('applications/', StudentApplicationsView.as_view(), name='applications'),

    path('', JobListView.as_view(), name='list'),
    path('<int:pk>/', JobDetailView.as_view(), name='detail'),
    path('api/', include(router.urls)),
]
