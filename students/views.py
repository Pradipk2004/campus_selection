# students/views.py
from django.contrib.auth.mixins import LoginRequiredMixin
from django.utils import timezone
from django.views.generic import TemplateView, ListView
from jobs.models import Job, Application
from interviews.models import Interview
from chat.models import Conversation, ChatMessage
from chat.models import ChatMessage
from django.views import View
from accounts.models import CustomUser
from django.shortcuts import render, get_object_or_404, redirect


class StudentDashboardView(LoginRequiredMixin, TemplateView):
    template_name = 'students/dashboard.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        today = timezone.now().date()
        
        context['jobs_count'] = Job.objects.count()
        context['apps_count'] = Application.objects.filter(student=user).count()
        context['next_interview'] = Interview.objects.filter(application__student=user, scheduled_at__date__gte=today).order_by('scheduled_at').first()
        context['recent_activities'] = Application.objects.filter(student=user).order_by('-applied_at')[:5]
        context['today'] = today

        return context

# -------------------------------
# Jobs List View
# -------------------------------
class StudentJobsListView(LoginRequiredMixin, ListView):
    def get(self, request):
        jobs = Job.objects.all()
        return render(request, 'jobs/jobs_list.html', {'jobs': jobs})

# -------------------------------
# Applications View
# -------------------------------
class StudentApplicationsView(LoginRequiredMixin, ListView):
    template_name = 'jobs/applications.html'
    context_object_name = 'applications'

    def get_queryset(self):
        # Correct field name: applied_at
        return Application.objects.filter(student=self.request.user).order_by('-applied_at')

# -------------------------------
# Interviews View
# -------------------------------
class StudentInterviewsView(LoginRequiredMixin, ListView):
    model = Interview
    template_name = "interviews/interviews.html"
    login_url = '/accounts/login/'

    def get_queryset(self):
        return Interview.objects.filter(
            application__student=self.request.user
        ).order_by("scheduled_at")

# -------------------------------
# Chat View
# -------------------------------
class StudentChatView(LoginRequiredMixin, View):
    def get(self, request):
        messages_list = ChatMessage.objects.filter(receiver=request.user) | ChatMessage.objects.filter(sender=request.user)
        messages_list = messages_list.order_by('timestamp')
        return render(request, 'chat/chat.html', {'messages': messages_list})

    def post(self, request):
        content = request.POST.get('message')
        if content:
            # Assuming student chats with all recruiters; adapt as needed
            recruiters = CustomUser.objects.filter(role='recruiter')
            for rec in recruiters:
                ChatMessage.objects.create(sender=request.user, receiver=rec, content=content, sender_type='student')
        return redirect('students:chat')

class StudentJobsView(LoginRequiredMixin, TemplateView):
    template_name = "students/jobs.html"
    login_url = '/accounts/login/'