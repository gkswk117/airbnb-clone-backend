from django.urls import path
from . import views
urlpatterns = [
    path('mypage', views.MyPage.as_view()),
]