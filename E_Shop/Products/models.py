from django.db import models
# ------CK Editors--------------------
from ckeditor.fields import RichTextField


#------For Slug Fild-----------------------------
from django.utils.text import slugify
from django.db.models.signals import pre_save


# Create your models here.
# ------------------------All Category Start-------------------------------------------------------------------------------
class Main_Category(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Category(models.Model):
    main_category = models.ForeignKey(Main_Category, on_delete=models.CASCADE, related_name="Category")
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name + "__" + self.main_category.name


class Sub_Category(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name="Sub_Category")
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name + "__" + self.category.name + "__" + self.category.main_category.name


# ------------------------All Category End-------------------------------------------------------------------------------

# ------------------------All Products Start-----------------------------------------------------------------------------

class Section(models.Model):
    name = models.CharField(max_length=100, null=True, blank=True)

    def __str__(self):
        return self.name


class Products(models.Model):
    Total_quantity = models.IntegerField(default=1)
    Availability = models.IntegerField(default=1)
    Image = models.CharField(max_length=200)
    Product_name = models.CharField(max_length=100)
    Price = models.IntegerField(default=0)
    Discount_Price = models.IntegerField(default=0)
    Discount = models.IntegerField(default=0)
    Product_information = RichTextField(null=True, blank=True)
    Tags = models.CharField(max_length=100, null=True, blank=True)
    Description = RichTextField(null=True, blank=True)

    slug = models.SlugField(default='', max_length=500, null=True, blank=True)
    main_category = models.ForeignKey(Main_Category, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    sub_category = models.ForeignKey(Sub_Category, on_delete=models.CASCADE, null=True, blank=True)
    section = models.ForeignKey(Section, on_delete=models.DO_NOTHING)

    def __str__(self):
        return self.Product_name
# --------------------------------For Add Slug Fild in Model Start------------------------------------------
    def get_absolute_url(self):
        from django.urls import reverse
        return reverse("Products_Details", kwargs={'slug': self.slug})

    class Meta:
        db_table = "app_Products"


def create_slug(instance, new_slug=None):
    slug = slugify(instance.Product_name)
    if new_slug is not None:
        slug = new_slug
    qs = Products.objects.filter(slug=slug).order_by('-id')
    exists = qs.exists()
    if exists:
        new_slug = "%s-%s" % (slug, qs.first().id)
        return create_slug(instance, new_slug=new_slug)
    return slug


def pre_save_post_receiver(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = create_slug(instance)

pre_save.connect(pre_save_post_receiver, Products)
# --------------------------------For Add Slug Fild in Model End------------------------------------------

class Product_Images(models.Model):
    product = models.ForeignKey(Products, on_delete=models.CASCADE, related_name="Product_Images")
    Image_url = models.CharField(max_length=200, null=True, blank=True)


class Additional_Information(models.Model):
    product = models.ForeignKey(Products, on_delete=models.CASCADE, related_name="Additional_Information")
    Specification = models.CharField(max_length=100, null=True, blank=True)
    detail = models.CharField(max_length=100, null=True, blank=True)

# ------------------------All Products End-------------------------------------------------------------------------------
