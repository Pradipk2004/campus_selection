# recruiters/urls.py
from django.urls import path
from . import views

app_name = 'recruiters'

urlpatterns = [
    path('dashboard/', views.RecruiterDashboardView.as_view(), name='dashboard'),

    # Jobs management
    path('jobs/', views.JobListView.as_view(), name='job_list'),
    path('jobs/create/', views.JobCreateView.as_view(), name='job_create'),

    # Applications & Interviews
    path('jobs/<int:job_id>/applications/', views.ApplicationsView.as_view(), name='applications'),
    path('applications/<int:application_id>/interview/', views.schedule_interview, name='schedule_interview'),  # ✅ ADD THIS
    path('interviews/<int:pk>/edit/', views.EditInterviewView.as_view(), name='edit_interview'),
    path('interviews/<int:pk>/cancel/', views.CancelInterviewView.as_view(), name='cancel_interview'),

    # Chat
    path('chat/', views.RecruiterChatView.as_view(), name='chat'),
]
