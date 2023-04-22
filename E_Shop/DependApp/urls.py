from django.urls import path
from django.views.decorators.csrf import csrf_exempt
from .views import Main_Cate, Cate

urlpatterns = [
    # path('Main_Cate/', Main_Cate, name="Main_Cate"),
    # path('Cate/', Cate, name="Cate"),


    path('Main_Cate/', Main_Cate.as_view()),
    path('Cate/', Cate.as_view()),
]