from django.shortcuts import render
from django.http import HttpResponse
from django.http import  JsonResponse
from django.core import serializers
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.exceptions import NotFound
from rest_framework.status import HTTP_204_NO_CONTENT
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet
from .models import Category
from .serializers import CategorySerializer
# Create your views here.
# (3) ViewSet
# 이제 본격적으로 django rest framework의 마법을 부릴 시간.

# (중요!!) view를 view_ViewSet.py로 쓸 때는 seializer를 serializers_new.py로 써야한다.
# serializers_previous.py의 Serializer는 첫번째 인자로 QuerySet이 들어온다는 가정하에 코드가 구성되어있다. 이를 테면 instance.update()메소드 사용함.
# 여기에서는 Serializer의 첫번째 인자로 a single object가 들어간다.

class CategoryViewSet(ModelViewSet):
    serializer_class = CategorySerializer
    queryset = Category.objects.all()

    # ㄴㅇㄱ 끝? 개.쩐.다. 단 세 줄. 이게 모두 ModelViewSet 덕분.
    # 근데 ModelSerializer는 그냥 모델의 형식을 가져오는것이므로 개꿀~하면서 맘껏 쓰면 되는데, (단순 복붙 작업을 없애줌.)
    # ViewSet은 사용할 때 고민을 해봐야 한다.
    # ViewSet이 정한 기능들(list, create, retrieve, partial_update, destroy...)에 추가 기능을 넣길 원한다면?
    # category를 지우기 전에 이메일을 보내고 싶거나, 사용가자 소유하고 있는 category만 retrieve하고 싶거나, 사용자가 host(관리자)인지 확인하고 싶거나, 사용자가 이메일 인증을 했는지 확인하고 싶거나 등등.
    # ViewSet을 커스텀해야되는 머리 아픈 상황이 발생. (워드프레스로 홈페이지 만들때 커스텀하는 과정을 상상해보셈.)
    # ViewSet을 커스텀하려면 어떻게 해야되는지 그 내부 코드를 들춰봐야되고 구글링도 해봐야되고... 오히려 더 귀찮음.
    # 커스터마이징하고 싶은 기능이 많으면 그냥 이전에 했던것 처럼 너가 코드를 다 작성하는게 더 좋을 수 있다.
    # 그래서 우리는 최종적으로 APIView를 사용할 것.