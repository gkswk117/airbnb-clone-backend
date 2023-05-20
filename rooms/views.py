from django.shortcuts import render
from django.http import HttpResponse
from .models import Room
# Create your views here.
def see_all_rooms(request):
    print(f"{request}\n")
    print(f"{dir(request)}\n")
    rooms = Room.objects.all()
    print(rooms[1].name)
    for each in rooms:
        print(each)
    return render(request, "all_rooms.html", {'rooms':rooms, 'title':'hello'})
# render 함수는 두번째 인자로 render할 html파일을 받고 그 파일을 자동으로 앱 폴더의 "templates" 폴더 내에서 찾는다.
# 그래서 폴더명을 너 마음대로 정할 수 없다.

def see_one_room(request, room_id):
    # url에서 변수를 넘겨받을 때, urls.py에 적힌 이름과 같은 이름을 써줘야 한다.
    print(room_id)
    print(Room.objects.get(pk=room_id))
    return HttpResponse("hi")