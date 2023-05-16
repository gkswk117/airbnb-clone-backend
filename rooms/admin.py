from django.contrib import admin
from .models import Room, Amenity
# Register your models here.
"""
admin.site.register(House)
"""
# (HW's memo ref Docs)If you are happy with the default admin interface, you don’t need to define a ModelAdmin object at all. Just write like this.

# If you want to custom the admin interface, write like these two ways.
"""
class HouseAdmin(admin.ModelAdmin):
    list_display = ("name","price","address")
    list_filter = ("name", "price")
    search_fields = ("name",)

admin.site.register(House, HouseAdmin)
"""
""" or use decorater. """
@admin.register(Room)
class RoomAdmin(admin.ModelAdmin):
    list_display=("name","price","kind","owner")
    list_filter=("country","city")
    readonly_fields=("created_at","updated_at")
@admin.register(Amenity)
class AdminAdmin(admin.ModelAdmin):
    readonly_fields=("created_at","updated_at")