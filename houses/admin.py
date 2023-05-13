from django.contrib import admin
from .models import House

# Register your models here.

@admin.register(House)
# decorater
class HouseAdmin(admin.ModelAdmin):
    list_display = ("name","price","address")
    list_filter = ("name", "price")
    search_fields = ("name",)