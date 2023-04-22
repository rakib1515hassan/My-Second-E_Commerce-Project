from django.shortcuts import render, redirect
from django.db.models import Q
import os
from django.http import Http404
from django.http import HttpResponseRedirect, HttpResponse, JsonResponse
from django.template.loader import render_to_string
from .models import *


# For Paginator--------------------------------------
from django.core.paginator import Paginator

# Redirect Function base view to Class base view-------------------------
from django.urls import reverse_lazy


#------------------------------------------------------------------------
from django.views.generic.base import TemplateView, RedirectView
# Display View-----------------------------------------------------------
from django.views import View
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView

# Editing View-----------------------------------------------------------
from django.views.generic import CreateView, UpdateView, DeleteView

# Aggregate  Function-----------------------------------------------------
# from django.db.models import Max, Min, Avg, Sum
from django.db.models import Avg, Max, Min

# Create your views here.

def base(request):
    return render(request, "index.html")

#------------------------------------------Home Page Render------------------------------------
# Function

# def home(request):
#     main_cats = Main_Category.objects.all()
#     product = Products.objects.filter(section__name="Top Deals Of The Day")
#     product_sell = Products.objects.filter(section__name="Top Selling Products")
#     product_Recommended = Products.objects.filter(section__name="Recommended For You")

#     shop = Main_Category.objects.all()[:5]


#     context = {
#         "main_cats": main_cats,
#         "product": product,
#         "product_sell": product_sell,
#         "product_Recommended": product_Recommended,
#         "shop": shop,
#     }
#     return render(request, "home.html", context)

# Class Base View
class home(TemplateView):
    template_name = "home.html"

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)

        # Pass data by template_context.py ---------------------------------------------------------
        # data['main_cats'] = Main_Category.objects.all()
        # data['product'] = Products.objects.filter(section__name="Top Deals Of The Day")
        # data['product_sell'] = Products.objects.filter(section__name="Top Selling Products")
        # data['product_Recommended'] = Products.objects.filter(section__name="Recommended For You")

        # data['shop'] = Main_Category.objects.all()[:5]

        return data


#--------------------------------------------------Product Detail-------------------------------------
# Function View

# def Products_Details(request, slug):
#     main_cats = Main_Category.objects.all()

#     product = Products.objects.filter(slug=slug)
#     if product.exists():
#         product = Products.objects.filter(slug=slug)
#     else:
#         return redirect("Error404")

#     data = {
#         "product": product,
#         "main_cats": main_cats,
#     }
#     return render(request, "Products/product-details.html", data)

# Class View
class Products_Details(DetailView):
    model = Products
    template_name = "Products/product-details.html"
    context_object_name = 'product'

    # slug_field = 'slug'
    # slug_url_kwarg = 'get_absolute_url'

    # def get_object(self, queryset=None):
    #     try:
    #         return super().get_object(queryset=queryset)
    #     except Http404:
    #         return redirect("Error404")

    def dispatch(self, request, *args, **kwargs):
        try:
            return super().dispatch(request, *args, **kwargs)
        except Http404:
            return redirect("Error404")

        
    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        # if not self.object:
        #     raise Http404("Product does not exist")
        data = self.get_context_data(object=self.object)
        # data['main_cats'] = Main_Category.objects.all()
        # data['shop'] = Main_Category.objects.all()[:5]
        return self.render_to_response(data)

    # def get_context_data(self, *args, **kwargs):
    #     data = super().get_context_data(**kwargs)
    #     data['main_cats'] = Main_Category.objects.all()
    #     return data
    

#--------------------------------------------Error 404 Page---------------------------------------------------

# def Error404(request):
#     return render(request, "404.html")


class Error404(TemplateView):
    template_name = "404.html"
    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        # data['main_cats'] = Main_Category.objects.all()
        # data['cats'] =Category.objects.all()
        # data['shop'] = Main_Category.objects.all()[:5]
        return data
    

#-----------------------------------------------All Product Show by Catagory-------------------------------------
# Function View

# def products_show(request, *args, **kwargs):
#     main_cats = Main_Category.objects.all()
#     cats =Category.objects.all()
#     minMaxPrice = Products.objects.aggregate(Max("Price"), Min("Price"))
#     products =Products.objects.all()
#     brand = ""

#     m_id = kwargs.get('m_id')
#     c_id = kwargs.get('c_id')
#     s_id = kwargs.get('s_id')
#     # print("-------------")
#     # print(m_id,c_id,s_id)
#     # print("-------------")

#     if (m_id !=None) and (c_id== None) and (s_id== None):
#         products = Products.objects.filter(main_category__id = m_id)
#         #brand = Sub_Category.objects.filter(category__id = c_id)
#         # print("----------------------")
#         # print(products)
#         # print("----------------------")
#         # q = Category.objects.filter(main_category__id=m_id)
        
#     elif (m_id!=None) and (c_id!=None) and (s_id==None):
#         products = Products.objects.filter(Q(main_category__id = m_id) & Q(category__id = c_id))
#         brand = Sub_Category.objects.filter(category__id = c_id)
#         # print("----------------------")
#         # print("id-2:",products)
#         # print("----------------------")
#     elif m_id and c_id and s_id:
#         products = Products.objects.filter(Q(main_category__id = m_id) & Q(category__id = c_id) & Q(sub_category__id = s_id))
#         brand = Sub_Category.objects.filter(category__id = c_id)
#         # print("----------------------")
#         # print("id-3:",products)
#         # print("----------------------")
#     else:
#         products =Products.objects.all()

#     # Pagination-------------------------------------------------
#     paginator = Paginator(products, 8)  # Show 25 contacts per page.
#     a = paginator.count
#     # print("Total Products =", a)
#     page_number = request.GET.get('page')
#     # print("Page Number =",page_number)
#     page_obj = paginator.get_page(page_number)
#     # print("Next =", page_obj)
#     nums = "a" * page_obj.paginator.num_pages
#     #-----------------------------------------------------------
    

#     data = {
#         "main_cats": main_cats,
#         "cats": cats,
#         # "products": products,
#         "minMaxPrice": minMaxPrice,
#         "brand": brand,

#         "page_number": page_number,
#         "page_obj": page_obj,
#         "nums": nums,
#     }
#     return render(request, "Products/shop.html", data)



## Class View
class products_show(ListView):
    template_name = "Products/shop.html"
    model = Products
    paginate_by = 12
    # context_object_name = 'products'
    
    def get_context_data(self, *args, **kwargs):
        data= super().get_context_data(**kwargs)
        data['minMaxPrice'] = Products.objects.aggregate(Max("Price"), Min("Price"))
        m_id = self.kwargs.get('m_id')
        c_id = self.kwargs.get('c_id')
        s_id = self.kwargs.get('s_id')
        # print("-------------")
        # print(m_id, c_id, s_id)
        # print("-------------")

        if (m_id !=None) and (c_id== None) and (s_id== None):
            data['brand']=""
        elif (m_id!=None) and (c_id!=None) and (s_id==None):
            data['brand'] = Sub_Category.objects.filter(category__id=c_id)
            # print("----------- S_id--------------")
            # print(data['brand'])
            # print("------------------------------")
        elif m_id and c_id and s_id:
            data['brand'] = Sub_Category.objects.filter(category__id=c_id)
            # print("----------- S_id--------------")
            # print(data['brand'])
            # print("------------------------------")
    
        return data
    
    def get_queryset(self):
        queryset = super().get_queryset()
        m_id = self.kwargs.get('m_id')
        c_id = self.kwargs.get('c_id')
        s_id = self.kwargs.get('s_id')

        if m_id:
            queryset = queryset.filter(main_category__id = m_id)
        if m_id and c_id:
            queryset = queryset.filter(Q(main_category__id = m_id) & Q(category__id = c_id))
        if m_id and c_id and s_id:
            queryset = queryset.filter(Q(main_category__id = m_id) & Q(category__id = c_id) & Q(sub_category__id = s_id))


        return queryset
    
#-----------------------------------------------Products Filter--------------------------------------------------------        



# def filter_data(request):
#     categories = request.GET.getlist('category[]')
#     sub_catagory = Sub_Category.objects.filter(category__id__in=categories)

#     brands = request.GET.getlist('brand[]')
#     if brands:    
#         Cat = Category.objects.filter(Sub_Category__id__in=brands)
#         sub_catagory = Sub_Category.objects.filter(category__id__in=Cat)


#     minPrice = request.GET['minPrice']
#     maxPrice = request.GET['maxPrice'] 

#     # print("--------------------------------------")
#     # print("catagory id=",categories)
#     # print("brand id =",brands)
#     # print("min price =",minPrice)
#     # print("max price =",maxPrice)
#     # print("--------------------------------------")

#     allProducts = Products.objects.all().order_by('-id').distinct()

#     allProducts = Products.objects.filter(Price__gte=minPrice)
#     allProducts = Products.objects.filter(Price__lte=maxPrice)
#     # print(allProducts)

#     if len(categories) > 0:
#         allProducts = allProducts.filter(category__id__in=categories).distinct()

#     if len(brands) > 0:
#         allProducts = allProducts.filter(sub_category__id__in=brands)
#     # pro = Paginator(allProducts, 8)


#     pro = render_to_string('Products/shop/product.html', {'page_obj': allProducts})
#     brand_s = render_to_string('Products/shop/brands.html', {'brand':sub_catagory})
    

#     return JsonResponse({'product_ajax': pro, 'brand_ajax':brand_s})




class filter_data(ListView):
    model = Products
    template_name = "Products\shop\shop.html"
    paginate_by = 8

    def get(self, request):
        categories = request.GET.getlist('category[]')
        sub_catagory = Sub_Category.objects.filter(category__id__in=categories)

        brands = request.GET.getlist('brand[]')
        if brands:    
            Cat = Category.objects.filter(Sub_Category__id__in=brands)
            sub_catagory = Sub_Category.objects.filter(category__id__in=Cat)


        minPrice = request.GET['minPrice']
        maxPrice = request.GET['maxPrice'] 

        # print("--------------------------------------")
        # print("catagory id=",categories)
        # print("brand id =",brands)
        # print("min price =",minPrice)
        # print("max price =",maxPrice)
        # print("--------------------------------------")

        allProducts = Products.objects.all().order_by('-id').distinct()

        allProducts = Products.objects.filter(Price__gte=minPrice)
        allProducts = Products.objects.filter(Price__lte=maxPrice)
        # print(allProducts)

        if len(categories) > 0:
            allProducts = allProducts.filter(category__id__in=categories).distinct()

        if len(brands) > 0:
            allProducts = allProducts.filter(sub_category__id__in=brands)
        # pro = Paginator(allProducts, 8)


        pro = render_to_string('Products/shop/product.html', {'page_obj': allProducts})
        brand_s = render_to_string('Products/shop/brands.html', {'brand':sub_catagory})

        return JsonResponse({'product_ajax': pro, 'brand_ajax':brand_s})
    
    def render_to_response(self,request, context, **response_kwargs):
        # Get the current page number
        page_number = self.request.GET.get('page')

        # Get the paginated data
        page_obj = context['page_obj']
        # Create a dictionary containing the paginated data and pagination links



        data = {
            'html': render_to_string(self.template_name, {'page_obj': page_obj}, request=self.request),
            'pagination': render_to_string('Products\shop\pagination.html', {'page_obj': page_obj}, request=self.request),
        }
        return JsonResponse(data)
    



# class filter_data(ListView):
#     model = Products
#     template_name = "Products/product.html"
#     paginate_by = 4

#     def get_queryset(self, request):
#         queryset = super().get_queryset()

#         # Apply filtering based on request parameters
#         categories = request.GET.getlist('category[]')
#         if categories:
#             queryset = queryset.filter(category__id__in=categories).distinct()

#         return queryset

    # def render_to_response(self, context, **response_kwargs):
    #     # Get the current page number
    #     page_number = self.request.GET.get('page')

    #     # Get the paginated data
    #     page_obj = context['page_obj']

    #     # Get the filtered data
    #     filtered_data = context['object_list']

    #     # Create a dictionary containing the paginated data, filtered data, and pagination links
    #     data = {
    #         'html': render_to_string(self.template_name, {'page_obj': page_obj, 'filtered_data': filtered_data}, request=self.request),
    #         'pagination': render_to_string('pagination.html', {'page_obj': page_obj}, request=self.request),
    #     }

    #     # Return the data as a JSON response
    #     return JsonResponse(data)

