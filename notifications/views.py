from django.views.generic import ListView
from django.shortcuts import redirect
from .models import Notification

class NotificationListView(ListView):
    model = Notification
    template_name = "notifications/list.html"

    def get_queryset(self):
        return Notification.objects.filter(user=self.request.user).order_by("-created_at")

def mark_as_read(request, pk):
    notif = Notification.objects.get(pk=pk, user=request.user)
    notif.is_read = True
    notif.save()
    return redirect("notifications:list")
