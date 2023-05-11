from django.db import models

# Create your models here.
# expressjs의 mongoose에서 Models의 User.js, Video.js와 같은 작업.

class House(models.Model):
    """ Model Definition for Houses """
    name = models.CharField(max_length=140)
    price = models.PositiveIntegerField()
    description = models.TextField()
    address = models.CharField(max_length=140)