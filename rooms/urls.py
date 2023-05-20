from django.urls import path
from .views import say_hello, say_hi
urlpatterns = [
    path('', say_hello),
    path('asdf', say_hi)
]