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
from django.conf.urls.static import static
from django.conf import settings
#from rooms.views import see_all_rooms
urlpatterns = [
    path('admin/', admin.site.urls),
    #path('rooms_test', see_all_rooms ),
    path('api/v1/categories/', include("categories.urls")),
    path('api/v1/rooms/', include("rooms.urls")),
    path('api/v1/experiences/', include("experiences.urls")),
    path('api/v1/tests/', include("testAPP.urls")),
    path('api/v1/medias/', include('medias.urls'))
    #include의 의미: rooms/~~ 로 오는 url은 모두 rooms.urls로 가시오.
    #nodejs, reactjs의 router 개념이랑 똑같음.
    #헷갈림 방지용으로 api를 위한 url을 api/{버전정보}를 앞에 붙여주기로 함.
] + static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)
# 브라우저가 MEDIA_URL로 가면 서버의 MEDIA_ROOT에 있는 파일을 보여주라는 것.
# https://docs.djangoproject.com/en/4.2/howto/static-files/#serving-files-uploaded-by-a-user-during-development
# 개발하는 환경에서는 상관없지만, 배포할 서버에서는 이렇게 하면 보안상의 문제가 있고, 디스크 용량 문제도 있다.
# https://docs.djangoproject.com/en/4.2/ref/settings/#std-setting-MEDIA_URL
# 그래서 사용자가 업로드 하는 파일은 다른 서버에 넣고, django 서버에는 파일이 저장된 외부 서버의 위치만 저장할 것.