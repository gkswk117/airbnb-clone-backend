from django.contrib import admin
from .models import Room, Amenity


@admin.action(description="Set all prices to zero")
def reset_prices(model_action, request, queryset):
    for each in queryset.all():
        print(each)
        print(type(each))
        each.price = 0
        each.save()


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
    list_display = (
        "name",
        "price",
        "rating_average",
        "orm_practice",
        "total_amenities_model",
        "total_amenities_admin",
        "kind",
        "owner",
    )
    # 함수를 추가시키면 return값을 패널에 display 해준다.
    # custom function은 models.py에서 정의하는 방법 / admin.py에서 정의하는 방법이 있다.
    # 이 admin 패널에서만 사용할거면 admin.py에 정의하고, 모델이 가는 어디든 이 함수를 사용할거면 model에 정의하기.
    list_filter = ("country", "city")
    readonly_fields = ("created_at", "updated_at")
    search_fields = (
        "name",
        "^price",
        "=owner__username",
    )

    # 8.2 Admin Actions
    actions = (reset_prices,)
    # admin panel의 액션에 함수를 추가
    # 액션에서 선택하여 실행하면 해당 함수가 호출된다.
    # 함수를 호출할 때, self, request, queryset 세 가지 argument를 넣어서 호출한다.
    # self에 이 함수를 호출한 admin를 넣는다. ex) rooms.RoomAdmin
    # requset에 이 요청을 보낸 사용자(user)에 대한 정보도 포함되어있는 request 정보를 넣는다.
    # queryset에 관리자가 admin panel에서 선택한 모델(인스턴스)를 배열로 만들어 넣는다.

    # 7.3 Admin Method
    # admin 패널에 있는 모든 메소드는 admin 패널에서 호출될 때 두 번째 매개변수로 모델의 인스턴스가 들어간다.
    def orm_practice(self, room):
        print("Room.objects.filter(created_at__year =2023) is !!!!!!!!!!!!!!!!!!")
        print(Room.objects.filter(created_at__year=2023))
        print(f"Room.objects is {Room.objects}")
        print(type(Room.objects))
        print("\n")
        return "orm_practice 입니다."

    def total_amenities_admin(self, room):
        print(f"total_amenities_admin 메소드의 두번째 인자인 room는 {room}")
        print(f"room.amenities is {room.amenities}")
        print(type(room.amenities))
        print("\n")
        return "total_amenities_admin 입니다. + " + str(room.amenities.count())


@admin.register(Amenity)
class AdminAdmin(admin.ModelAdmin):
    readonly_fields = ("created_at", "updated_at")
