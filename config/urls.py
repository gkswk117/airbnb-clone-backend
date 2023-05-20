"""
URL configuration for config project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from rooms.views import say_hello
urlpatterns = [
    path('admin/', admin.site.urls),
    #path('rooms', say_hello )
    path('rooms/', include("rooms.urls"))
    #include의 의미: rooms/~~ 로 오는 url은 모두 rooms.urls로 가시오.
    #nodejs, reactjs의 router 개념이랑 똑같음.
]
