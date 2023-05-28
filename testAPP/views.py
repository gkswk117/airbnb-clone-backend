from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.exceptions import NotFound
from rest_framework.status import HTTP_204_NO_CONTENT
from .models import Test
from .serializers import TestSerializer
# Create your views here.
# (2) rest api for react

class SeeAllTests(APIView):
    def get(self,request):
        all_test = Test.objects.all()
        serializer = TestSerializer(all_test, many=True)
        return Response(serializer.data)
    def post(self,request):
        serializer = TestSerializer(data=request.data)
        if serializer.is_valid():
            new_test= serializer.save()
            return Response(TestSerializer(new_test).data)
        else:
            return Response(serializer.errors)
        
class SeeOneTests(APIView):
    def get_object(self, pk):
        one_category=Test.objects.get(pk=pk)
        return one_category
    def get(self, request, pk):
        serializer = TestSerializer(self.get_object(pk))
        return Response({'ok':True, 'category':serializer.data})
    def put(self, request, pk):
        serializer = TestSerializer(self.get_object(pk), data=request.data, partial = True)
        # serializer의 첫번째 인수로 왜 Query set을 줄 수 없는가?
        # 그야 ModelSerializer가 a single object만 받겠다는데. 니가 왜 딴지거냐?
        # 꼬우면 니가 직접 커스텀 Serializer를 구현하던지.
        if serializer.is_valid():
            saved_test = serializer.save()
            return Response(TestSerializer(saved_test).data)
        else:
            return Response(serializer.errors)
    def delete(self, request, pk):
        self.get_object(pk).delete()
        return Response(status=HTTP_204_NO_CONTENT)