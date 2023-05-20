from django.shortcuts import render
from django.http import HttpResponse
from .models import Room
# Create your views here.
def see_all_rooms(request):
    print(f"{request}\n")
    print(f"{dir(request)}\n")
    for each in Room.objects.all():
        print(each)
    return HttpResponse("hello")

def see_one_room(request, room_id):
    # url에서 변수를 넘겨받을 때, urls.py에 적힌 이름과 같은 이름을 써줘야 한다.
    print(room_id)
    print(Room.objects.get(pk=room_id))
    return HttpResponse("hi")