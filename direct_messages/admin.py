from django.contrib import admin
from .models import ChatRoom, Message
# Register your models here.
@admin.register(ChatRoom)
class ChatRoomAdmin(admin.ModelAdmin):
    list_display = ("__str__", "created_at", "updated_at",)
@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ("text","participant","chat_room","created_at",)
