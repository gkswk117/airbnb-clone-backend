from django.urls import path
from . import views
# config/urls.py에서 /wishlists/~~ 경로는 모두 이쪽으로 가라고 설정함.
urlpatterns = [
    path("", views.Wishlists.as_view())
]