from channels.generic.websocket import AsyncJsonWebsocketConsumer
from channels.db import database_sync_to_async
from django.contrib.auth.models import AnonymousUser

from accounts import models
from .models import Conversation, Message

class ChatConsumer(AsyncJsonWebsocketConsumer):
    async def connect(self):
        user = self.scope["user"]
        if isinstance(user, AnonymousUser):
            await self.close()
            return
        self.conversation_id = int(self.scope["url_route"]["kwargs"]["conversation_id"])
        if not await self.user_in_conversation(user.id, self.conversation_id):
            await self.close(); return
        self.group_name = f"conv_{self.conversation_id}"
        await self.channel_layer.group_add(self.group_name, self.channel_name)
        await self.accept()

    async def receive_json(self, content, **kwargs):
        user = self.scope["user"]
        text = content.get("text","")
        msg_id = await self.save_message(user.id, self.conversation_id, text)
        await self.channel_layer.group_send(self.group_name, {"type":"chat.message","msg_id":msg_id,"text":text,"sender":user.id})

    async def chat_message(self, event):
        await self.send_json(event)

    async def disconnect(self, code):
        await self.channel_layer.group_discard(self.group_name, self.channel_name)

    @database_sync_to_async
    def user_in_conversation(self, user_id, conv_id):
        return Conversation.objects.filter(id=conv_id).filter(models.Q(student_id=user_id)|models.Q(recruiter_id=user_id)).exists()

    @database_sync_to_async
    def save_message(self, user_id, conv_id, text):
        return Message.objects.create(conversation_id=conv_id, sender_id=user_id, text=text).id
