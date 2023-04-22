from django.contrib import admin
from .models import *


# Register your models here.

class Product_Image_Admin(admin.TabularInline):
    model = Product_Images


class Additional_Information_Admin(admin.TabularInline):
    model = Additional_Information


class Products_Admin(admin.ModelAdmin):
    inlines = (Product_Image_Admin, Additional_Information_Admin)
    list_display = ('Product_name', 'Price', 'category', 'section')
    list_editable = ('category', 'section')
    class Media:
        js=("admin.js",)


admin.site.register(Section)
admin.site.register(Products, Products_Admin)
admin.site.register(Product_Images)
admin.site.register(Additional_Information)


class Main_Category_Admin(admin.TabularInline):
    model = Main_Category


class Sub_Category_Admin(admin.TabularInline):
    model = Sub_Category


class Category_Admin(admin.ModelAdmin):
    inlines = (Sub_Category_Admin,)
    #list_display = ('name',)
#     # list_editable = ()


admin.site.register(Main_Category)
admin.site.register(Category, Category_Admin)
admin.site.register(Sub_Category)
