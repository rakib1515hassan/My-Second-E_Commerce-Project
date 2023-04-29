from .models import Main_Category, Products, Category, Sub_Category

# Aggregate  Function-----------------------------------------------------
from django.db.models import Max, Min, Avg, Sum

def common(request):
    pass
    main_cats = Main_Category.objects.all()
    cats =Category.objects.all()
    sub_cats =Sub_Category.objects.all()
    product = Products.objects.filter(section__name="Top Deals Of The Day")

    product_sell = Products.objects.filter(section__name="Top Selling Products")
    product_Recommended = Products.objects.filter(section__name="Recommended For You")
    shop = Main_Category.objects.all()[:5]

    
    data = {
        "main_cats":main_cats,
        "cats":cats,
        "sub_cats":sub_cats,        
        "product":product,

        "product_sell":product_sell,
        "product_Recommended":product_Recommended,
        "shop":shop,

    }
    return data