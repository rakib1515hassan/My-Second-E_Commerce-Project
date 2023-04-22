from django.shortcuts import render
from Products.models import *
from Products.views import *

# Create your views here.
from django.http.response import JsonResponse
from rest_framework.views import APIView
#from rest_framework.decorators import api_view
from rest_framework.permissions import IsAuthenticated


class Main_Cate(APIView):
    permission_classes=[IsAuthenticated,]
    def post(self,request,format=None):
        main_cate=request.data['main_cate']
        cate={}
        if main_cate:
            cate_s=Main_Category.objects.get(id=main_cate).Category.all()
            cate={p.name:p.id for p in cate_s}
        return JsonResponse(data=cate, safe=False)

class Cate(APIView):
    permission_classes=[IsAuthenticated,]
    def post(self,request,format=None):
        cate=request.data['cate']
        sub_cate={}
        if cate:
            sub_cate_s=Category.objects.get(id=cate).Sub_Category.all()
            sub_cate={p.name:p.id for p in sub_cate_s}
        return JsonResponse(data=sub_cate, safe=False)

# @api_view(['POST'])
# def Main_Cate(request):
#     main_cate = request.data['main_cate']
#     # permission_classes = [IsAuthenticated, ]
#     cate = {}
#     if main_cate:
#         cate_s = Main_Category.objects.get(id=main_cate).Category.all()
#         cate = {p.name: p.id for p in cate_s}
#     return JsonResponse(data=cate, safe=False)


# @api_view(['GET', 'POST'])
# def hello_world(request):
#     if request.method == 'POST':
#         return Response({"message": "Got some data!", "data": request.data})
#     return Response({"message": "Hello, world!"})


# @api_view(['POST'])
# def Cate(requset):
#     cate = request.data['cate']
#     print(cate)
#     # permission_classes = [IsAuthenticated, ]
#     sub_cate = {}
#     if cate:
#         sub_cate_s = Category.objects.get(id=cate).Sub_Category.all()
#         sub_cate = {p.name: p.id for p in sub_cate_s}
#     return JsonResponse(data=sub_cate, safe=False)
