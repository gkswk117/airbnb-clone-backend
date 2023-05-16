from django.db import models
from common.models import CommonModel
# Create your models here.
class Category(CommonModel):
    """Room or Experience Category"""
    name= models.CharField(max_length=50)
    class CategoryKindChoices(models.TextChoices):
        ROOMS= ("rooms", "Rooms")
        EXPERIENCES = "experiences", "Experiences"
    kind = models.CharField(max_length=50, choices=CategoryKindChoices.choices)
    def __str__(self):
       return f"{self.kind}: {self.name}"
