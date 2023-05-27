from django.urls import path
from . import views_previous
from . import views
urlpatterns = [
    #path('', views.see_all_categories),
    path('', views.SeeAllCategories.as_view()),
    path('html', views_previous.categories_html),
    path('react', views_previous.categories_for_react),
    #path('<int:pk>', views.see_one_category)
    path('<int:pk>', views.SeeOneCategory.as_view())
]