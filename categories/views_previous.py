from django.shortcuts import render
from django.http import HttpResponse
from django.http import  JsonResponse
from django.core import serializers
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.exceptions import NotFound
from rest_framework.status import HTTP_204_NO_CONTENT
from .models import Category
from .serializers import CategorySerializer
# Create your views here.
# Django rest Framework를 사용하기 전에 수동적으로 하는 방법을 먼저 배울 것.

# noob
# django template을 이용해 바로 html로 렌더링.
def categories_html(request):
    all_categories= Category.objects.all()
    print(all_categories[0].name)
    # super noob
    # return HttpResponse("post!!!")
    return render(request, "html.html", {'potatos':all_categories, 'title':'모든 카테고리 리스트입니다.'})
    
# pro
# 다이나믹 UI를 구현하는데 reactjs만한게 없다. 바로 렌더링 하는게 아니라 서버에서는 json 형식의 데이터를 보내기만(response하기만) 한다.
def categories_for_react(request):
    all_categories= Category.objects.all()
    print(all_categories[0].name)
    return JsonResponse({'ok':True, "categories":serializers.serialize("json",all_categories)})
    # serializers가 django QuerySet 형식을 json 형식으로 바꿔준다. user가 post할 때는 반대 방향으로도 바꿔준다.
    # django QuerySet<=>json
    # 1) 이렇게 하면 내가 선택적으로 category데이터를 전달해주지 못함. 모두다 전달됨. 이걸 customizing 하고 싶음.
    # => serializer를 customizing한다. serializers.py 참고. 이땐 api_view 굳이 필요 없음.
    # 2) 그리고 전달받은 json 파일을 좀더 이쁘게 보고싶음.
    # => api_view() decorator

# hacker
@api_view(['GET', 'POST'])
# 빈칸으로 비워두면 디폴트로 get request만 받음.
# 이렇게 하면 get request와 post request 모두 받겠다고 설정하는것.
def see_all_categories(request):
    if request.method == "GET":
        all_categories= Category.objects.all()
        serializer = CategorySerializer(all_categories, many=True)
        # 여기서 CategorySerializer는 우리가 커스터마이징한 serializer이다. 
        return Response({'ok':True,'categories':serializer.data})
        # Response함수를 쓰려면 api_view() decorator가 있어야 한다.
        # api_view() decorator가 없으면 JsonResponse로 못생긴 json을 받으면 된다.
    elif request.method == "POST":
        print(request.data)
        serializer = CategorySerializer(data=request.data)
        # json => Query Set 으로 변환하기 위해서는 data=을 붙여줘야 한다.
        if serializer.is_valid():
            new_category = serializer.save()
            return Response(CategorySerializer(new_category).data,)
        else: 
            return Response(serializer.errors)

@api_view(['GET','PUT', 'DELETE'])
# GET이나 POST로 put, delete를 대체할 수 있지만 서버간 보내는 신호, 약속 정도로 생각해주면 된다.
def see_one_category(request, pk):
    one_category=Category.objects.filter(pk=pk)
    if not len(one_category):
        raise NotFound
        # return이랑 raise랑 다른점. return은 status code를 200으로 보내지만, raise는 raise 옆에 적힌 에러 코드(NotFound의 경우 404)를 보낸다.
    if request.method == 'GET':
        serializer = CategorySerializer(one_category, many=True)
        return Response({'ok':True, 'category':serializer.data})
    elif request.method == 'PUT':
        serializer = CategorySerializer(one_category, data=request.data, partial = True)
        # partial=True는 required=True를 무시할 수 있게 해준다. 일부만 보내겠다는 뜻.
        if serializer.is_valid():
            updated_count = serializer.save()
            return Response({"updated_count":updated_count})
            #return Response(CategorySerializer(new_category).data)
        else:
            return Response(serializer.errors)
    elif request.method == "DELETE":
        one_category.delete()
        return Response(status=HTTP_204_NO_CONTENT)