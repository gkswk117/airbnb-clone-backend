from django.db import models
from common.models import CommonModel


# Create your models here.
class Experience(CommonModel):
    """Experience Model Definition"""

    name = models.CharField(max_length=180, default="")
    country = models.CharField(max_length=50, default="한국")
    city = models.CharField(max_length=80, default="서울")
    price = models.PositiveIntegerField()
    description = models.TextField()
    address = models.CharField(max_length=250)
    host = models.ForeignKey(
        "users.User",
        on_delete=models.CASCADE,
    )
    start = models.TimeField()
    end = models.TimeField()
    perks = models.ManyToManyField("experiences.Perk")
    category = models.ForeignKey(
        "categories.Category",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )

    def __str__(self):
        return self.name


class Perk(CommonModel):
    name = models.CharField(max_length=180, default="")
    short_description = models.CharField(max_length=250, default="", blank=True)
    description = models.TextField(default="", blank=True)

    def __str__(self):
        return self.name
