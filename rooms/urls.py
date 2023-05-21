from django.urls import path
from .views import see_all_rooms, see_one_room
urlpatterns = [
    path('', see_all_rooms),
    path('<int:room_pk>', see_one_room)
]