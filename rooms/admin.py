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
    list_display=("name","price","rating_average","orm_practice","total_amenities_model","total_amenities_admin","kind","owner")
    list_filter=("country","city")
    readonly_fields=("created_at","updated_at")
    # admin 패널에 있는 모든 메소드는 admin 패널에서 호출될 때 두 번째 매개변수로 모델의 인스턴스가 들어간다.
    def orm_practice(self, room):
        print(Room.objects.filter(created_at__year =2023))
        print(f"Room.objects is {Room.objects}")
        print(type(Room.objects))
        print("\n")
        return "orm_practice 입니다."
    def total_amenities_admin(self, room):
        print(f"total_amenities_admin 메소드의 두번째 인자인 room는 {room}")
        print(f"room.amenities is {room.amenities}")
        print(type(room.amenities))
        print("\n")
        return "total_amenities_admin 입니다. + "+str(room.amenities.count())
@admin.register(Amenity)
class AdminAdmin(admin.ModelAdmin):
    readonly_fields=("created_at","updated_at")