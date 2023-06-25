from django.urls import path
from . import views
urlpatterns = [
    path('', views.CreateUser.as_view()),
    path('mypage', views.MyPage.as_view()),
    path('change-password', views.ChangePassword.as_view()),
    path('log-in', views.LogIn.as_view()),
    path('log-out', views.LogOut.as_view()),
    path('@<str:username>', views.SeeOneUser.as_view())
]