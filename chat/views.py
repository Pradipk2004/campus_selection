from django.views.generic import ListView,TemplateView
from .models import Conversation
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect
from .models import ChatMessage
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from accounts.models import CustomUser

@login_required
def student_chat(request):
    messages_list = ChatMessage.objects.filter(receiver=request.user) | ChatMessage.objects.filter(sender=request.user)
    messages_list = messages_list.order_by('timestamp')

    if request.method == 'POST':
        content = request.POST.get('message')
        if content:
            recruiters = CustomUser.objects.filter(role='recruiter')
            for rec in recruiters:
                ChatMessage.objects.create(sender=request.user, receiver=rec, content=content, sender_type='student')
        return redirect('chat:student_chat')

    return render(request, 'chat/student_chat.html', {'messages': messages_list})

@login_required
def recruiter_chat(request):
    messages_list = ChatMessage.objects.filter(receiver=request.user) | ChatMessage.objects.filter(sender=request.user)
    messages_list = messages_list.order_by('timestamp')

    if request.method == 'POST':
        content = request.POST.get('message')
        if content:
            students = CustomUser.objects.filter(role='student')
            for student in students:
                ChatMessage.objects.create(sender=request.user, receiver=student, content=content, sender_type='recruiter')
        return redirect('chat:recruiter_chat')

    return render(request, 'chat/recruiter_chat.html', {'messages': messages_list})



class ChatView(LoginRequiredMixin, TemplateView):
    template_name = 'chat/chat.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['messages'] = ChatMessage.objects.filter(student=self.request.user).order_by('-timestamp')
        return context

    def post(self, request, *args, **kwargs):
        message = request.POST.get('message')
        if message:
            ChatMessage.objects.create(student=request.user, sender_type='student', content=message)
        return redirect('students:chat')
    
class ConversationListView(ListView):
    model = Conversation
    template_name = "chat/conversation_list.html"

    def get_queryset(self):
        return Conversation.objects.filter(student=self.request.user)

class MessageListView(ListView):
    model = ChatMessage
    template_name = "chat/messages_list.html"

    def get_queryset(self):
        conv_id = self.kwargs["pk"]
        return ChatMessage.objects.filter(conversation_id=conv_id).order_by("sent_at")
