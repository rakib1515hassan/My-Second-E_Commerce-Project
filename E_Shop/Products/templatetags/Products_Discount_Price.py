from django import template
import math

register = template.Library()


@register.simple_tag
def products_discount_calculate(Price, Discount):
    if Discount is None or Discount is 0:
        return Price
    Descount_pric = Price
    Descount_pric = Price - (Price * Discount / 100)
    # pro= Products.objects.all()
    # pro.Discount_Price=Descount_pric
    # pro.save()
    return math.floor(Descount_pric)


@register.simple_tag
def progress_bar_quantity(Availability, Total_quantity):
    progress_Bar = Availability
    progress_Bar = Availability * (100/Total_quantity)
    return progress_Bar