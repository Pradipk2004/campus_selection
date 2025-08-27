# chat/admin.py
from django.contrib import admin
from .models import ChatMessage

@admin.register(ChatMessage)
class ChatMessageAdmin(admin.ModelAdmin):
    list_display = ('sender', 'receiver', 'sender_type', 'timestamp')
    list_filter = ('sender_type',)
    search_fields = ('sender__username', 'receiver__username', 'content')
