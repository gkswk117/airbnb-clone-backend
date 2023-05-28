from django.shortcuts import render
from django.http import HttpResponse
from django.http import  JsonResponse
from django.core import serializers
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.exceptions import NotFound
from rest_framework.status import HTTP_204_NO_CONTENT
from rest_framework.views import APIView
from .models import Category
from .serializers import CategorySerializer
# Create your views here.
# (2) APIView
# django rest framework의 APIView를 이용해 좀 더 코드를 깔끔하게 바꿀 수 있다. (리팩토링)

# (중요!!) view를 view_APIView.py로 쓸 때는 seializer를 serializers_previous.py로 써야한다.
# serializers_new.py의 ModelSerializer는 첫번째 인자로 무조건 single object만 받는다.
# 여기에서는 Serializer의 첫번째 인자로 QuerySet을 넘겨줬다.

class SeeAllCategories(APIView):
    # APIView가 사용자의 요청 메소드에 따라 request를 자동으로 라우팅 해준다.
    # if, elif 쓸 필요 없다.
    # 예를 들면, get request가 오면 "get" method 호출.
    def get(self, request):
        all_categories= Category.objects.all()
        serializer = CategorySerializer(all_categories, many=True)
        return Response({'ok':True,'categories':serializer.data})
    def post(self, request):
        print(request.data)
        serializer = CategorySerializer(data=request.data)
        if serializer.is_valid():
            new_category = serializer.save()
            return Response(CategorySerializer(new_category).data,)
        else: 
            return Response(serializer.errors)

class SeeOneCategory(APIView):
    def get_queryset(self, pk):
        one_category=Category.objects.filter(pk=pk)
        if not len(one_category):
            raise NotFound
        return one_category
    def get(self, request, pk):
        serializer = CategorySerializer(self.get_queryset(pk), many=True)
        return Response({'ok':True, 'category':serializer.data})
    def put(self, request, pk):
        serializer = CategorySerializer(self.get_queryset(pk), data=request.data, partial = True)
        # partial=True는 required=True를 무시할 수 있게 해준다. 일부만 보내겠다는 뜻.
        if serializer.is_valid():
            updated_count = serializer.save()
            return Response({"updated_count":updated_count})
            #return Response(CategorySerializer(new_category).data)
        else:
            return Response(serializer.errors)
    def delete(self, request, pk):
        self.get_queryset(pk)[0].delete()
        # self.get_queryset(pk).delete()
        # 둘 다 된다. 왜냐하면 Model.delete() 메소드도 있고, QuerySet.delete() 메소드도 있기 때문.
        return Response(status=HTTP_204_NO_CONTENT)