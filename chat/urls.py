from django.urls import path
from . import views
from .views import ChatView, student_chat, recruiter_chat

app_name = "chat"

urlpatterns = [
    path('chat/', ChatView.as_view(), name='chat'),
    path('student/', views.student_chat, name='student_chat'),
    path('recruiter/', views.recruiter_chat, name='recruiter_chat'),
    path("conversations/", views.ConversationListView.as_view(), name="conversations"),
    path("conversations/<int:pk>/", views.MessageListView.as_view(), name="messages"),
]
