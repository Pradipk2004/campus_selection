# interviews/urls.py
from django.urls import path
from . import views

app_name = "interviews"

urlpatterns = [
    path("interviews/", views.InterviewListView.as_view(), name="interviews"),
    path("my-interviews/", views.student_interviews, name="student_interviews"),
    #path("create/", views.create_interview, name="create"),
    path("<int:pk>/", views.InterviewDetailView.as_view(), name="detail"),
    #path("<int:pk>/edit/", views.edit_interview, name="edit"),
    path("<int:pk>/cancel/", views.cancel_interview, name="cancel"),
]
