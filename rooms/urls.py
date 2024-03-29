from django.urls import path
from . import views

# config/urls.py에서 /rooms/~~ 경로는 모두 이쪽으로 가라고 설정함.
urlpatterns = [
    # path('', views.see_all_rooms),
    # path('<int:room_pk>', views.see_one_room),
    path("", views.SeeAllRooms.as_view()),
    path("<int:pk>", views.SeeOneRoom.as_view()),
    path("<int:pk>/reviews", views.RoomReviews.as_view()),
    path("<int:pk>/photos", views.RoomPhotos.as_view()),
    path("<int:pk>/bookings", views.RoomBookings.as_view()),
    path("amenities/", views.SeeAllAmenities.as_view()),
    path("amenities/<int:pk>", views.SeeOneAmenity.as_view()),
]
