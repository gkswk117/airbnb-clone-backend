from django.db import models
from common.models import CommonModel
# Create your models here.
"""
채팅방. 하나의 방에는 많은 유절들이 참석할 수 있다.
메세지. 메세지는 한 명의 유저로부터 만들어져서 방으로 보내질 것.
"""
class ChatRoom(CommonModel):
    """ChatRoom Model Definition"""
    participants = models.ManyToManyField("users.User")
class Message(CommonModel):
    """Message Model Definition""" 
    text = models.TextField()
    participant = models.ForeignKey("users.User", on_delete=models.SET_NULL, null=True, blank=True)
    chat_room = models.ForeignKey("direct_messages.ChatRoom", on_delete=models.CASCADE)
    def __str__(self):
        return f"{self.participant}: {self.text}"