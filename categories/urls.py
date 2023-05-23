from django.urls import path
from .views import categories_html, categories_for_react, see_all_categories, see_one_category
urlpatterns = [
    path('', see_all_categories),
    path('html', categories_html),
    path('react', categories_for_react),
    path('<int:pk>', see_one_category)
]