# accounts/views.py

from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import CreateView, ListView
from django.contrib.auth import login
from django.contrib.auth.views import LoginView, LogoutView
from django.urls import reverse_lazy
from django.contrib import messages
from django.contrib.auth.decorators import login_required

from .forms import (
    CustomUserRegisterForm,
    StudentProfileForm,
    RecruiterProfileForm,
    EditProfileForm,
)
from .models import (
    CustomUser,
    StudentProfile,
    RecruiterProfile,
    StudentDocument,
)


# -------------------
# Register View
# -------------------
class RegisterView(CreateView):
    model = CustomUser
    form_class = CustomUserRegisterForm
    template_name = "accounts/register.html"
    success_url = reverse_lazy("home")

    def form_valid(self, form):
        user = form.save()  # ✅ save once, signals handle profile creation
        login(self.request, user)

        # Redirect based on role
        if user.role == CustomUser.STUDENT:
            return redirect("students:dashboard")
        elif user.role == CustomUser.RECRUITER:
            return redirect("recruiters:dashboard")
        elif user.role == CustomUser.ADMIN:
            return redirect("admin:index")

        return redirect(self.success_url)

    def get_success_url(self):
        return self.success_url


# -------------------
# Custom Login View
# -------------------
class CustomLoginView(LoginView):
    template_name = "accounts/login.html"

    def get_success_url(self):
        user = self.request.user
        if user.role == CustomUser.STUDENT:
            return reverse_lazy("students:dashboard")
        elif user.role == CustomUser.RECRUITER:
            return reverse_lazy("recruiters:dashboard")
        elif user.role == CustomUser.ADMIN:
            return reverse_lazy("admin:index")
        return reverse_lazy("home")


# -------------------
# Custom Logout View
# -------------------
class CustomLogoutView(LogoutView):
    next_page = "home"


# -------------------------------
# Profile Edit
@login_required
def edit_profile(request):
    user = request.user

    # Select profile model & form depending on role
    if user.role == CustomUser.STUDENT:
        profile, _ = StudentProfile.objects.get_or_create(user=user)
        ProfileFormClass = StudentProfileForm
    elif user.role == CustomUser.RECRUITER:
        profile, _ = RecruiterProfile.objects.get_or_create(user=user)
        ProfileFormClass = RecruiterProfileForm
    else:
        messages.error(request, "Invalid role. Cannot edit profile.")
        return redirect("home")

    if request.method == "POST":
        user_form = EditProfileForm(request.POST, instance=user)
        profile_form = ProfileFormClass(request.POST, request.FILES, instance=profile)

        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()

            # Preserve files if no new file uploaded
            profile_instance = profile_form.save(commit=False)
            for field in ["resume", "certifications", "profile_picture"]:
                if hasattr(profile, field) and field not in request.FILES:
                    setattr(profile_instance, field, getattr(profile, field))
            profile_instance.save()

            messages.success(request, "✅ Profile updated successfully!")
            return redirect("accounts:edit_profile")
        else:
            messages.error(request, "⚠️ Please correct the errors below.")

    else:
        user_form = EditProfileForm(instance=user)
        profile_form = ProfileFormClass(instance=profile)

    return render(
        request,
        "accounts/edit_profile.html",
        {"form": user_form, "profile_form": profile_form},
    )



# -------------------------------
# Student Documents (CRUD)
# -------------------------------
class StudentDocumentListView(ListView):
    model = StudentDocument
    template_name = "accounts/documents_list.html"

    def get_queryset(self):
        return StudentDocument.objects.filter(user=self.request.user)


@login_required
def upload_document(request):
    if request.method == "POST":
        file = request.FILES.get("document")
        if file:
            
            allowed_types = [
                "application/pdf",
                "application/msword",
                "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
            ]
            if file.content_type not in allowed_types:
                messages.error(request, "Only PDF or Word documents are allowed.")
                return redirect("accounts:upload_document")

            StudentDocument.objects.create(user=request.user, file=file)
            messages.success(request, "Document uploaded successfully!")
            return redirect("accounts:documents")

    return render(request, "accounts/upload_document.html")


@login_required
def delete_document(request, pk):
    doc = get_object_or_404(StudentDocument, pk=pk, user=request.user)
    doc.delete()
    messages.success(request, "Document deleted successfully!")
    return redirect("accounts:documents")
