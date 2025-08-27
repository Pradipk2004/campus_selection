from django.urls import path
from . import views, api
from django.contrib.auth import views as auth_views

app_name = "accounts"

urlpatterns = [
    # Unified registration view for both students and recruiters
    path("register/", views.RegisterView.as_view(), name="register"),

    path("login/", views.CustomLoginView.as_view(), name="login"),
    path("logout/", views.CustomLogoutView.as_view(), name="logout"),
    path("profile/edit/", views.edit_profile, name="edit_profile"),
    path("resume-feedback/", api.my_resume_feedback, name="resume_feedback"),
    path("documents/", views.StudentDocumentListView.as_view(), name="documents"),
]
