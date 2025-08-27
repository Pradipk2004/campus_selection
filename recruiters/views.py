from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import View
from django.contrib.auth.decorators import login_required
from jobs.models import  Application
from .forms import JobForm
from interviews.forms import InterviewForm
from jobs.models import Job
from interviews.models import Interview
from chat.models import ChatMessage
from django.contrib import messages

# Dashboard
class RecruiterDashboardView(LoginRequiredMixin, View):
    def get(self, request):
        jobs_count = Job.objects.filter(recruiter=request.user).count()
        applications_count = Application.objects.filter(job__recruiter=request.user).count()
        interviews_count = Interview.objects.filter(application__job__recruiter=request.user).count()
        unread_messages = ChatMessage.objects.filter(receiver=request.user).count()
        context = {
            'jobs_count': jobs_count,
            'applications_count': applications_count,
            'interviews_count': interviews_count,
            'unread_messages': unread_messages,
        }
        return render(request, 'recruiters/dashboard.html', context)

# Job list / create
class JobListView(LoginRequiredMixin, View):
    def get(self, request):
        jobs = Job.objects.filter(recruiter=request.user)
        return render(request, 'recruiters/job_list.html', {'jobs': jobs})

class JobCreateView(LoginRequiredMixin, View):
    def get(self, request):
        form = JobForm()
        return render(request, 'recruiters/job_create.html', {'form': form})
    
    def post(self, request):
        form = JobForm(request.POST)
        if form.is_valid():
            job = form.save(commit=False)
            job.recruiter = request.user
            job.save()
            return redirect('recruiters:job_list')
        return render(request, 'recruiters/job_create.html', {'form': form})

# View applications for a job
class ApplicationsView(LoginRequiredMixin, View):
    def get(self, request, job_id):
        job = get_object_or_404(Job, id=job_id, recruiter=request.user)
        applications = Application.objects.filter(job=job)
        return render(request, 'recruiters/applications.html', {'job': job, 'applications': applications})

@login_required
def schedule_interview(request, application_id):
    application = get_object_or_404(Application, id=application_id)
    existing_interview = Interview.objects.filter(application=application).first()

    if existing_interview:
        return render(request, "interviews/create.html", {
            "interview_exists": existing_interview
        })

    if request.method == "POST":
        form = InterviewForm(request.POST)
        if form.is_valid():
            interview = form.save(commit=False)
            interview.application = application
            interview.save()
            messages.success(request, "Interview scheduled successfully!")
            return redirect("interview_detail", interview.id)
    else:
        form = InterviewForm()

    return render(request, "interviews/create.html", {
        "form": form,
        "interview_exists": None
    })



class EditInterviewView(LoginRequiredMixin, View):
    def get(self, request, pk):
        interview = get_object_or_404(Interview, pk=pk, application__job__recruiter=request.user)
        form = InterviewForm(instance=interview, recruiter=request.user)
        return render(request, "recruiters/edit_interview.html", {"form": form, "interview": interview})

    def post(self, request, pk):
        interview = get_object_or_404(Interview, pk=pk, application__job__recruiter=request.user)
        form = InterviewForm(request.POST, instance=interview, recruiter=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, "Interview updated successfully.")
            return redirect("recruiters:applications", job_id=interview.application.job.id)
        return render(request, "recruiters/edit_interview.html", {"form": form, "interview": interview})
    
class CancelInterviewView(LoginRequiredMixin, View):
    def post(self, request, pk):
        interview = get_object_or_404(Interview, pk=pk, application__job__recruiter=request.user)
        interview.status = "Cancelled"
        interview.save()
        messages.info(request, "Interview cancelled.")
        return redirect("recruiters:applications", job_id=interview.application.job.id)
# Chat view
class RecruiterChatView(LoginRequiredMixin, View):
    def get(self, request):
        messages = ChatMessage.objects.filter(sender=request.user) | ChatMessage.objects.filter(receiver=request.user)
        messages = messages.order_by('timestamp')
        return render(request, 'recruiters/chat.html', {'messages': messages})

    def post(self, request):
        content = request.POST.get('message')
        receiver_id = request.POST.get('receiver_id')
        # Assume student receiver
        from django.contrib.auth import get_user_model
        User = get_user_model()
        receiver = get_object_or_404(User, id=receiver_id)
        ChatMessage.objects.create(
            sender=request.user,
            receiver=receiver,
            content=content,
            sender_type='recruiter'
        )
        return redirect('recruiters:chat')
