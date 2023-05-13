from django.db import models

# Create your models here.
# expressjs의 mongoose에서 Models의 User.js, Video.js와 같은 작업.

class House(models.Model):
    """ Model Definition for Houses """
    name = models.CharField(max_length=140)
    price = models.PositiveIntegerField()
    description = models.TextField()
    address = models.CharField(max_length=140)
    def __str__(self):
        return self.name
    #2.5 에서 배웠던 내용. 클래스를 print할 때 내가 원하는 것으로 출력하고 싶으면 __str__메서드의 리턴값에 집어넣기.
    # underscroe method에 대한 자세한 내용은 네이버 메모 참고


# 4.1 Migration
# 모델을 만들고 python manage.py makemigrations으로 migration만들어주기.
# 그리고 python manage.py migrate으로 생성된 migration파일을 데이터베이스에 적용시켜주기
# 모델을 수정할 때도 항상 위와 같은 과정을 거쳐야 한다.