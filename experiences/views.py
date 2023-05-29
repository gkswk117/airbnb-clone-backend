from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.status import HTTP_204_NO_CONTENT
from rest_framework.exceptions import NotFound
from .models import Perk
from .serializer import PerkSerializer
# Create your views here.
class SeeAllPerks(APIView):
    def get(self, request):
        all_perks = Perk.objects.all()
        return Response(PerkSerializer(all_perks, many=True).data)
    def post(self, request):
        serializer = PerkSerializer(data=request.data)
        # (수정하고 싶은 인스턴스, data=수정할 데이터) => Serializer의 update() 메소드 실행
        # (data=수정할 데이터) => Serializer의 create() 메소드 실행
        # json => Model
        if serializer.is_valid():
            new_perk = serializer.save()
            return Response(PerkSerializer(new_perk).data)
        else:
            return Response(serializer.errors)

class SeeOnePerk(APIView):
    def get_object(self, pk):
        try:
            one_perk = Perk.objects.get(pk=pk)
            return one_perk
        except Perk.DoesNotExist:
            raise NotFound
    def get(self, requset, pk):
        # url로 get request를 받으면 해당 클래스의 get()메소드가 실행이 되고, django는 알아서 get(req, param)을 넣어서 보내준다.
        return Response(PerkSerializer(self.get_object(pk)).data)
    def put(self, requset, pk):
        serializer =  PerkSerializer(self.get_object(pk), data=requset.data, partial=True)
        # (수정하고 싶은 인스턴스, data=수정할 데이터)를 받은 serializer => save() 메소드 호출 시 update() 메소드 호출
        # (data=수정할 데이터)를 받은 serializer => save() 메소드 호출 시 create() 메소드 호출
        if serializer.is_valid():
            updated_perk = serializer.save()
            # serializer.save()를 하면 저장된 or 업데이트된 모델 인스턴스를 반환한다.
            return Response(PerkSerializer(updated_perk).data)
        else:
            return Response(serializer.errors)
    def delete(self, requset, pk):
        self.get_object(pk).delete()
        return Response(status=HTTP_204_NO_CONTENT)