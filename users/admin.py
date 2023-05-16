from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User

# Register your models here.

@admin.register(User)
# decorater
class UserAdmin(UserAdmin):
# 다른 모델과 다르게 유저 모델에 최적화된 admin panel을 상속받을 것.
# 다른 모델은 admin.ModelAdmin을 상속 받음.
    list_display = ("username","name", "email", "is_host")
    fieldsets = (
        ("Profile", {"fields":("username", "password", "name","email","is_host","avatar","gender","language","currency")}),
        ("Permissions",{"fields": ("is_active","is_staff","is_superuser","groups","user_permissions",),},),
        ("Important dates", {"fields": ("last_login", "date_joined"), "classes":("collapse",)},)
    )