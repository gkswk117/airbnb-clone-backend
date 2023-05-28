from django.db import models
from django.db import models
from common.models import CommonModel
# Create your models here.

class Test(CommonModel):
    """Room or Experience Category"""
    name= models.CharField(max_length=50)
    created_att = models.CharField(max_length=50, default="defualt")
    kind = models.DateTimeField(auto_now_add=True)