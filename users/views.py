import jwt
from django.conf import settings
from django.contrib.auth import authenticate, login, logout
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
        
class LogIn(APIView):
    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')
        if not username or not password:
            raise ParseError
        user= authenticate(request, username=username, password=password)
        # django가 자동으로 비밀번호 hash화 해서 유저를 찾아줄 것임.
        if user:
            login(request, user)
            # 단 한 줄로 django는 user를 로그인 시킬 것.
            # 자동으로 백엔드에서 user 정보가 담긴 session을 생성하고, 사용자에게 cookie를 보내줄 것.
            return Response({"ok":"Welcome"})
        else:
            return Response({"error":"wrong password"})
        
class LogOut(APIView):
    permission_classes = [IsAuthenticated]
    def post(self, request):
        logout(request)
        # 단 한 줄로 django는 user를 로그아웃 시킬 것.
        return Response({"ok":"Logged out!"})

class JWTLogIn(APIView):
    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')
        if not username or not password:
            raise ParseError
        user= authenticate(request, username=username, password=password)
        if user:
            """We have to sign the token here"""
            token = jwt.encode({"pk":user.pk}, settings.SECRET_KEY, algorithm="HS256")
            print("done!!!!!!!!!")
            return Response({'token':token})
        else:
            return Response({"error":"wrong password"})