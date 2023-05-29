from django.urls import path
from . import views
urlpatterns = [
    path('perks/', views.SeeAllPerks.as_view()),
    path('perks/<int:pk>', views.SeeOnePerk.as_view()),
]