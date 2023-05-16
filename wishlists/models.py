from django.db import models
from common.models import CommonModel
# Create your models here.
class Wishlist(CommonModel):
    """Wishlist Model Definition"""
    name = models.CharField(max_length=150,)
    room = models.ManyToManyField("rooms.Room")
    experience = models.ManyToManyField("experiences.Experience")
    user = models.ForeignKey("users.User", on_delete=models.CASCADE)
    def __str__(self):
       return self.name