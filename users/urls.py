from django.urls import path
from rest_framework.authtoken.views import obtain_auth_token
from . import views
urlpatterns = [
    path('', views.CreateUser.as_view()),
    path('mypage', views.MyPage.as_view()),
    path('change-password', views.ChangePassword.as_view()),
    path('log-in', views.LogIn.as_view()),
    path('log-out', views.LogOut.as_view()),
    path('token-login', obtain_auth_token),
    path('@<str:username>', views.SeeOneUser.as_view())
]