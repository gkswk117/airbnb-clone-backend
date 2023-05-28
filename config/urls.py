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
#from rooms.views import see_all_rooms
urlpatterns = [
    path('admin/', admin.site.urls),
    #path('rooms_test', see_all_rooms ),
    path('api/v1/rooms/', include("rooms.urls")),
    path('api/v1/categories/', include("categories.urls")),
    path('api/v1/tests/', include("testAPP.urls"))
    #include의 의미: rooms/~~ 로 오는 url은 모두 rooms.urls로 가시오.
    #nodejs, reactjs의 router 개념이랑 똑같음.
    #헷갈림 방지용으로 api를 위한 url을 api/{버전정보}를 앞에 붙여주기로 함.
]
