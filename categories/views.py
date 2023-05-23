from django.shortcuts import render
from django.http import  JsonResponse
from django.core import serializers
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Category
# Create your views here.
# Django rest Framework를 사용하기 전에 수동적으로 하는 방법을 먼저 배울 것.

# noob
def categories_noob(request):
    all_categories= Category.objects.all()
    # return render(request, "hhh.html", {'categories':all_categories, 'title':'모든 카테고리 리스트입니다.'})
    return JsonResponse({'ok':True, "categories":serializers.serialize("json",all_categories)})
    # serializers가 all_categories를 json 형식으로 바꿔준다.

# pro
@api_view()
def categories(request):
    return Response({'ok':True,})