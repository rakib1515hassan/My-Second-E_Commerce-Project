from django.urls import path
from django.views.decorators.csrf import csrf_exempt
from .views import *

urlpatterns = [
    path("base/", base, name="base"),


    # path("", home, name="home"),
    path("", home.as_view(), name="home"),


    #path("Products_Details/<slug:slug>/", Products_Details, name="Products_Details"),
    path("Products_Details/<slug:slug>/", Products_Details.as_view(), name="Products_Details"),
    #path("Products_Details/<int:pk>/", Products_Details.as_view, name="Products_Details"),


    # path("products_show/<int:m_id>/", products_show, name="products_show"),
    # path("products_show/<int:m_id>/<int:c_id>/", products_show, name="products_show"),
    # path("products_show/<int:m_id>/<int:c_id>/<int:s_id>/", products_show, name="products_show"),

    path("products_show/<int:m_id>/", products_show.as_view(), name="products_show"),
    path("products_show/<int:m_id>/<int:c_id>/", products_show.as_view(), name="products_show"),
    path("products_show/<int:m_id>/<int:c_id>/<int:s_id>/", products_show.as_view(), name="products_show"),



    # path('filter/',filter_data,name="filter-data"),
    path('filter/',filter_data.as_view(),name="filter-data"),
    



    #path("404/", Error404, name="Error404"),
    path("404/", Error404.as_view(), name="Error404"),
]