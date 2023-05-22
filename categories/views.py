from django.shortcuts import render
from django.http import  JsonResponse
from .models import Category
# Create your views here.
def categories(request):
    all_categories= Category.objects.all()
    #return render(request, "hhh.html", {'categories':all_categories, 'title':'모든 카테고리 리스트입니다.'})
    return JsonResponse({'ok':True})