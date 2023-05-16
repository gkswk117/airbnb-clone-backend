from django.db import models
from common.models import CommonModel
# Create your models here.

class Review(CommonModel):
    """Review from a User to a Room or Experience Model Definition"""
    user = models.ForeignKey("users.User", null=True, on_delete=models.SET_NULL)
    room = models.ForeignKey("rooms.Room", null=True, blank=True, on_delete=models.CASCADE)
    experience = models.ForeignKey("experiences.Experience", null=True, blank=True, on_delete=models.CASCADE)
    payload = models.TextField()
    rating = models.PositiveIntegerField()
    def __str__(self):
       return f"{self.user} / ✨{self.rating}"