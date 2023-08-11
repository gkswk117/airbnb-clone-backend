import jwt
import requests
from django.conf import settings
from django.contrib.auth import authenticate, login, logout
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.exceptions import ParseError
from rest_framework.exceptions import (
    NotFound,
    NotAuthenticated,
    ParseError,
    PermissionDenied,
)
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from .models import User
from .serializers import PrivateUserSerializer, TinyUserSerializer

GITHUB_CLIENT_ID = "ba5320afbf14928eed15"
KAKAO_REDIRECT_URI = "http://127.0.0.1:3000/social/kakao"
KAKAO_REST_API_KEY = "7d35aa0fff16fddde96a780601c654aa"
KAKAO_REQUEST_TOKEN_URL = "https://kauth.kakao.com/oauth/token"
KAKAO_UNLINK_URL = "https://kapi.kakao.com/v1/user/unlink"
KAKAO_REQ_USER_INFO_URL = "https://kapi.kakao.com/v2/user/me"


# Create your views here.
class IsLoggedIn(APIView):
    def get(self, request):
        user = request.user
        return Response({"result": user.is_authenticated})


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
        password = request.data.get("password")
        if not password:
            raise ParseError
        serializer = PrivateUserSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            # password는 save()메소드 안에 넣어주는게 아니라 AbstractUser 클래스의 set_password() 메소드를 이용할 것.
            user.set_password(password)
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
        return Response(TinyUserSerializer(user).data)


class ChangePassword(APIView):
    permission_classes = [IsAuthenticated]

    def put(self, request):
        user = request.user
        old_password = request.data.get("old-password")
        new_password = request.data.get("new-password")
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
        username = request.data.get("username")
        password = request.data.get("password")
        if not username or not password:
            raise ParseError
        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            return Response({"result": "DoesNotExist"})
        user = authenticate(request, username=username, password=password)
        # django가 자동으로 비밀번호 hash화 해서 유저를 찾아줄 것임.
        if user:
            login(request, user)
            # 단 한 줄로 django는 user를 로그인 시킬 것.
            # 자동으로 백엔드에서 user 정보가 담긴 session을 생성하고, 사용자에게 cookie를 보내줄 것.
            return Response({"result": "Success"})
        else:
            return Response({"result": "wrong password"})


class LogOut(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        access_token = request.user.kakao_access_token
        logout(request)
        # 단 한 줄로 django는 user를 로그아웃 시킬 것.
        id = requests.post(
            KAKAO_UNLINK_URL,
            headers={
                "Content-Type": "application/x-www-form-urlencoded",
                "Authorization": f"Bearer {access_token}",
            },
        )
        return Response({"ok": "Logged out!"})


class JWTLogIn(APIView):
    def post(self, request):
        username = request.data.get("username")
        password = request.data.get("password")
        if not username or not password:
            raise ParseError
        user = authenticate(request, username=username, password=password)
        if user:
            """We have to sign the token here"""
            token = jwt.encode({"pk": user.pk}, settings.SECRET_KEY, algorithm="HS256")
            return Response({"token": token})
        else:
            return Response({"error": "wrong password"})


class GithubLogIn(APIView):
    def post(self, request):
        github_token = request.data.get("code")
        # frontend의 api.ts에서 보낸 github token
        access_token = requests.post(
            f"https://github.com/login/oauth/access_token?code={github_token}&client_id={GITHUB_CLIENT_ID}&client_secret={settings.GH_SECRET}",
            headers={"Accept": "application/json"},
        )
        # django server에서 github에 보내는 post request.
        # headers={"Access":"application/json"}를 추가해줘서 json response를 리턴값으로 받는다.
        access_token = access_token.json().get("access_token")
        user_data = requests.get(
            "https://api.github.com/user",
            headers={
                "Authorization": f"Bearer {access_token}",
                "Accept": "application/json",
            },
        )
        user_data = user_data.json()
        # print("★★★★★★★ user_data is ★★★★★★★")
        # print(user_data)
        user_email = requests.get(
            "https://api.github.com/user/emails",
            headers={
                "Authorization": f"Bearer {access_token}",
                "Accept": "application/json",
            },
        )
        user_email = user_email.json()
        try:
            user = User.objects.get(email=user_email[0]["email"])
            serializer = PrivateUserSerializer(
                user,
                {"social_login": "github"},
                partial=True,
            )
            if serializer.is_valid():
                user = serializer.save()
                login(request, user)
                return Response(status=status.HTTP_200_OK)
            else:
                return Response(serializer.errors)
        except User.DoesNotExist:
            user = User.objects.create(
                name=user_data.get("name"),
                username="github#" + str(user_data.get("id")),
                email=user_email[0]["email"],
                avatar=user_data.get("avatar_url"),
                social_login="github",
            )
            user.set_unusable_password()
            # print(user.has_usable_password)  # 소셜 로그인하는 유저인지, 일반 유저인지 판단할 수 있다.
            user.save()
            login(request, user)
            return Response(status=status.HTTP_200_OK)


class KakaoLogIn(APIView):
    def post(self, request):
        kakao_code = request.data.get("code")
        # frontend의 api.ts에서 보낸 kakao 인가 코드
        access_token = requests.post(
            KAKAO_REQUEST_TOKEN_URL,
            headers={"Content-Type": "application/x-www-form-urlencoded"},
            data={
                "grant_type": "authorization_code",
                "code": kakao_code,
                "client_id": KAKAO_REST_API_KEY,
                "redirect_uri": KAKAO_REDIRECT_URI,
            },
        )

        access_token = access_token.json().get("access_token")
        user_data = requests.get(
            KAKAO_REQ_USER_INFO_URL,
            headers={
                "Authorization": f"Bearer {access_token}",
                "Content-type": "application/x-www-form-urlencoded;charset=utf-8",
            },
        )
        user_data = user_data.json()
        try:
            user = User.objects.get(email=user_data.get("kakao_account").get("email"))
            serializer = PrivateUserSerializer(
                user,
                {"social_login": "kakao", "kakao_access_token": access_token},
                partial=True,
            )
            if serializer.is_valid():
                user = serializer.save()
                login(request, user)
                return Response(status=status.HTTP_200_OK)
            else:
                return Response(serializer.errors)
        except User.DoesNotExist:
            user = User.objects.create(
                username="kakao#" + str(user_data.get("id")),
                name=user_data.get("kakao_account").get("profile").get("nickname"),
                email=user_data.get("kakao_account").get("email"),
                avatar=user_data.get("kakao_account")
                .get("profile")
                .get("profile_image_url"),
                social_login="kakao",
            )
            user.set_unusable_password()
            # print(user.has_usable_password)  # 소셜 로그인하는 유저인지, 일반 유저인지 판단할 수 있다.
            user.save()
            login(request, user)
            return Response(status=status.HTTP_200_OK)
