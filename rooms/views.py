from django.shortcuts import render
from django.http import HttpResponse
# Create your views here.
def say_hello(request):
    print(f"{request}\n")
    print(f"{dir(request)}\n")
    return HttpResponse("hello")

def say_hi(request):
    return HttpResponse("hi")