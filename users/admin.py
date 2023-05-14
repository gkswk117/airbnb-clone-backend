from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User

# Register your models here.

@admin.register(User)
# decorater
class UserAdmin(UserAdmin):
# House model과 다르게 유저 모델에 최적화된 admin panel을 상속받을 것.
    pass