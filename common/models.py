from django.db import models

# Create your models here.
class CommonModel(models.Model):
    """Common Model Definition"""
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    class Meta:
        abstract = True
    # 이 모델을 데이터베이스에 추가하지 말라는 코드.
    # 코드 재사용을 위해 만든 모델임.