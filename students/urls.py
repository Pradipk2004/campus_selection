from django.urls import path
from . import views

app_name = "students"

urlpatterns = [
    path("dashboard/", views.StudentDashboardView.as_view(), name="dashboard"),
    path("jobs/", views.StudentJobsListView.as_view(), name="jobs_list"),
    path("applications/", views.StudentApplicationsView.as_view(), name="applications"),
    path("interviews/", views.StudentInterviewsView.as_view(), name="interviews"),
    path("chat/", views.StudentChatView.as_view(), name="chat"),
    path('jobs/', views.StudentJobsView.as_view(), name='jobs'),
]
