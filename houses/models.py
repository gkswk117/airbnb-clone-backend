from django.db import models

# Create your models here.
# expressjs의 mongoose에서 Models의 User.js, Video.js와 같은 작업.

class House(models.Model):
    """ Model Definition for Houses """
    name = models.CharField(max_length=140)
    price = models.PositiveIntegerField()
    description = models.TextField()
    address = models.CharField(max_length=140, help_text='Korean address')
    owner = models.ForeignKey("users.User", on_delete=models.CASCADE)
    # 5.5 Foreign Key
    # MongoDB의 populate와 같은 기능.
    # 다른 모델의 아이디 타입을 ForeignKey라고 한다.
    # First argument => "{application이름}.{model이름}"
    # on_delete => owner에 ID가 저장된 모델이 삭제되었을때 House 모델은 어떻게 할 것인지.
    def __str__(self):
        return self.name
    #2.5 에서 배웠던 내용. 클래스를 print할 때 내가 원하는 것으로 출력하고 싶으면 __str__메서드의 리턴값에 집어넣기.
    # underscroe method에 대한 자세한 내용은 네이버 메모 참고

# 4.1 Migration
# 모델을 만들고 python manage.py makemigrations으로 migration만들어주기.
# 그리고 python manage.py migrate으로 생성된 migration파일을 데이터베이스에 적용시켜주기
# 모델을 수정할 때도 항상 위와 같은 과정을 거쳐야 한다.

# User model을 customizing하는 방법은 두가지.
# 1) 추가하고 싶은 field를 따로 만들어서(예를 들면 profile을 새로 만들어서) 기존의 장고 user model에 연결짓는 방법.
# 2) 아예 새로 User model을 만드는 방법.