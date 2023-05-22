from django.urls import path
from .views import see_all_rooms, see_one_room
# config/urls.py에서 /rooms/~~ 경로는 모두 이쪽으로 가라고 설정함.
urlpatterns = [
    path('', see_all_rooms),
    path('<int:room_pk>', see_one_room)
]