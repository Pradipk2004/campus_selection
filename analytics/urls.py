from django.urls import path
from . import views

app_name = "analytics"

urlpatterns = [
    path('student/', views.StudentAnalyticsView.as_view(), name='student_analytics'),
    path('recruiter/', views.RecruiterAnalyticsView.as_view(), name='recruiter_analytics'),
    path("performance/", views.my_performance, name="performance"),
]
