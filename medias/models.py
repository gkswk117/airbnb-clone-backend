from django.db import models
from common.models import CommonModel
# Create your models here.
class Photo(CommonModel):
    """"""
    file = models.ImageField()
    description = models.CharField(max_length=140,)
    room = models.ForeignKey("rooms.Room", on_delete=models.CASCADE, null=True, blank=True)
    experience = models.ForeignKey("experiences.Experience",on_delete=models.CASCADE, null=True, blank=True)

class Video(CommonModel):
    """room은 Video를 가질 수 없다. experience만 Video를 가지고, 이때 단 하나의 Video만 가진다."""
    file = models.FileField()
    description = models.CharField(max_length=140,)
    experience = models.OneToOneField("experiences.Experience",on_delete=models.CASCADE, null=True, blank=True)
    
    