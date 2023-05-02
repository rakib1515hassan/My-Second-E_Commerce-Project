from django.contrib import admin

# Register your models here.
## For Custom AbstructBaseUser-------------------------------------------------------
from django.contrib.auth.models import Group
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

from Accounts.models import User, Customer, Seller, UserOTP, Customer_Address
from .forms import UserCreationForm,UserChangeForm
# from .models import User

# # Register your models here.
# User = get_user_model



class UserAdmin(BaseUserAdmin):
    # The forms to add and change user instances
    add_form = UserCreationForm
    form = UserChangeForm

    list_display = ["email", "first_name", "last_name", "is_admin","is_customer","is_seller"]
    list_filter = ["is_admin"]
    fieldsets = [
        (None, {"fields": ["email", "password"]}),
        ("Personal info", {"fields": ["first_name", "last_name", "mobile"]}),
        ("Permissions", {"fields": ["is_active", "is_superuser", "is_admin","is_customer","is_seller"]}),
    ]
    # add_fieldsets is not a standard ModelAdmin attribute. UserAdmin
    # overrides get_fieldsets to use this attribute when creating a user.
    add_fieldsets = [
        (
            None,
            {
                "classes": ["wide"],
                "fields": ["email", "first_name", "last_name", "mobile", "password1", "password2","is_active"],
            },
        ),
    ]
    search_fields = ["email"]
    ordering = ["email"]
    filter_horizontal = []


admin.site.unregister(Group)
admin.site.register(User,UserAdmin)
admin.site.register(Customer)
admin.site.register(Seller)
admin.site.register(UserOTP)
admin.site.register(Customer_Address)