from django.shortcuts import render
from django.http import HttpResponse
from .models import Room
# Create your views here.
# (1) django templates
# Section 9 URLS AND VIEWS 코드

def see_all_rooms(request):
    print(f"{request}\n")
    print(f"{dir(request)}\n")
    rooms = Room.objects.all()
    print(rooms[1].name)
    for each in rooms:
        print(each)
    return render(request, "all_rooms.html", {'rooms':rooms, 'title':'모든 방 리스트입니다.'})
# render 함수는 두번째 인자로 render할 html파일을 받고 그 파일을 자동으로 앱 폴더의 "templates" 폴더 내에서 찾는다.
# 그래서 폴더명을 너 마음대로 정할 수 없다.

def see_one_room(request, room_pk):
    # url에서 변수를 넘겨받을 때, urls.py에 적힌 이름과 같은 이름을 써줘야 한다.
    # javascript의 try, catch 구문이랑 비슷하다.
    try:       
        room = Room.objects.get(pk=room_pk)
        print(2/0)
        # print(2/0)의 위치가 앞이면 ZeroDivisionError 에러가 전달,
        # room = Room.objects.get(pk=room_pk)의 위치가 앞이면 Room.DoesNotExist 에러가 전달된다.
        print(room_pk)
        print(room)
        print(dir(Room.DoesNotExist))
        return render(request, "one_room.html", {'room':room, 'error_code':1})
    except Room.DoesNotExist:
        #Room.DoesNotExist는 에러의 한 종류
        #Room.DoesNotExist라는 에러가 발생 했을때 이 블록을 실행한다.
        #에러의 종류 중에는 ZeroDivisionError, IndexError 등 여러 가지가 있고, Room.DoesNotExist는 그 중 하나이다.
        #참고: https://blog.naver.com/star7sss/222444006350
        return render(request, "one_room.html", {'error_code':2})
    except ZeroDivisionError:
        return render(request, "one_room.html", {'error_code':3})
    