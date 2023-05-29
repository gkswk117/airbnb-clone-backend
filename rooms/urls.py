from django.urls import path
from . import views
# config/urls.py에서 /rooms/~~ 경로는 모두 이쪽으로 가라고 설정함.
urlpatterns = [
    # path('', views.see_all_rooms),
    # path('<int:room_pk>', views.see_one_room),
    path('amenities/', views.SeeAllAmenities.as_view()),
    path('amenities/<int:pk>', views.SeeOneAmenity.as_view()),
]