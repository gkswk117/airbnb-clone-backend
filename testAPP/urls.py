from django.urls import path
from . import views
urlpatterns = [
    path('',views.SeeAllTests.as_view()),
    path('<int:pk>',views.SeeOneTests.as_view()),
]