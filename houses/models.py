from django.db import models

# Create your models here.
# expressjs의 mongoose에서 Models의 User.js, Video.js와 같은 작업.

class House(models.Model):
    """ Model Definition for Houses """
    name = models.CharField(max_length=140)
    price = models.PositiveIntegerField()
    description = models.TextField()
    address = models.CharField(max_length=140)

# 4.1 Migration
# 모델을 만들고 python manage.py makemigrations으로 migration만들어주기.
# 그리고 python manage.py migrate으로 생성된 migration파일을 데이터베이스에 적용시켜주기
# 모델을 수정할 때도 항상 위와 같은 과정을 거쳐야 한다.