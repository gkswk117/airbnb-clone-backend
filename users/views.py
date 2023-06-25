from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.exceptions import ParseError
from rest_framework.exceptions import NotFound, NotAuthenticated, ParseError, PermissionDenied
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from .models import User
from .serializers import PrivateUserSerializer, TinyUserSerializer

# Create your views here.
class MyPage(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request):
        user = request.user
        return Response(PrivateUserSerializer(user).data)
    def put(self, request):
        user = request.user
        serializer = PrivateUserSerializer(user, data=request.data, partial=True)
        if serializer.is_valid():
            user = serializer.save()
            return Response(PrivateUserSerializer(user).data)
        else:
            return Response(serializer.errors)

class CreateUser(APIView):
    def post(self, request):
        password = request.data.get('password')
        if not password:
            raise ParseError
        serializer = PrivateUserSerializer(data=request.data)
        if serializer.is_valid():
            print("이건됨?")
            user = serializer.save()
            # password는 save()메소드 안에 넣어주는게 아니라 AbstractUser 클래스의 set_password() 메소드를 이용할 것.
            user.set_password(password)
            print("이건됨???")
            user.save()
            
            # 이러면 django는 자동으로 password를 hash화 시켜준다.
            return Response(PrivateUserSerializer(user).data)
        else:
            return Response(serializer.errors)

class SeeOneUser(APIView):
    def get(self, request, username):
        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            raise NotFound
        print(user)
        return Response(TinyUserSerializer(user).data)
 
class ChangePassword(APIView):
    permission_classes = [IsAuthenticated]
    def put(self, request):
        user = request.user
        old_password = request.data.get('old-password')
        new_password = request.data.get('new-password')
        if not old_password or not new_password:
            raise ParseError
        if user.check_password(old_password):
        # AbstractUser의 check_password() 메소드를 이용할 것.
            user.set_password(new_password)
            user.save()
            return Response(status=status.HTTP_200_OK)
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)