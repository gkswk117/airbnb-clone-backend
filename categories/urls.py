from django.urls import path
from . import views_previous
from . import views
urlpatterns = [
    #path('', views.see_all_categories),
    #path('', views.SeeAllCategories.as_view()),
    path('', views.CategoryViewSet.as_view({'get':'list','post':'create'})),
    #get request가 오면 ViewSet의 list메소드 실행, post request가 오면 ViewSet의 create메소드 실행.
    path('html', views_previous.categories_html),
    path('react', views_previous.categories_for_react),
    #path('<int:pk>', views.see_one_category)
    #path('<int:pk>', views.SeeOneCategory.as_view())
    path('<int:pk>', views.CategoryViewSet.as_view({'get':'retrieve','put':'partial_update','delete':'destroy'})),
]