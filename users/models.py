from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.
class User(AbstractUser):
    first_name = models.CharField(max_length=10, editable=False)
    last_name = models.CharField(max_length=10, editable=False)
    # editable=False만 하면 에러뜸. admin페이지에서도 없애줘야 한다. 그러기 위해 admin.py에서 fieldsets를 오버라이딩함.
    name = models.CharField(max_length=20, default="")
    is_host = models.BooleanField(default="False")
    # 이렇게 하면 이전의 record(row, 데이터)에는 모두 default 값이 들어갈 것.
    # or is_host = models.BooleanField(null=True)
    avatar=models.URLField(blank=True)
    class GenderChoices(models.TextChoices):
        MALE = ("male", "Male")
        FEMALE = ("female", "Female")
    gender = models.CharField(max_length=10, choices=GenderChoices.choices,)
    class LanguageChoices(models.TextChoices):
        KR = ("kr", "Korean")
        EN = ("en", "English")
        # ("데이터베이스에 들어갈 value", "admin 패널에 보이게 될 value")
    language = models.CharField(max_length=10, choices=LanguageChoices.choices,)
    class CurrencyChoices(models.TextChoices):
        WON = "won", "Korean Won"
        USD = "usd", "Dollar"
        # Tuple을 적을때, ()를 생략해도 된다.
    currency = models.CharField(max_length=10, choices=CurrencyChoices.choices)

# House model은 완전히 처음부터 우리가 다 만들어서 models.Model라고 빈 껍데기만 상속 받았음.
# 하지만 User model은 Django의 user model의 속성 및 메소드를 모두 상속받을 것. CTRL+클릭 하면 속성 및 메서드를 모두 확인할 수 있다.
# Django의 user model에서 굳이 뭘 더 수정할게 없어도, 이렇게 User model을 새로 만들어서 상속을 받아 쓰는게 훨씬 좋고, 공식 문서에서도 이렇게 하는걸 적극 추천하고 있다.
# 그래야 나중에 내가 수정할 부분이 필요해졌을때 수정할 수 있다.
# 이제 우리는 Django가 제공하는 모든 것들을 가지고 있으면서, 필요에 의해 조작할 수 있게 되었다.
# 새로 User model을 추가하려면 기존의 데이터베이스를 삭제해야 하고, 각 migration file을 모두 삭제 해야 한 뒤 다시 python manage.py makemigrations, python manage.py migrate 해야한다.