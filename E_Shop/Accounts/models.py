from django.db import models
from django.contrib.auth.models import User

# Create your models here.
# class User_Profile(models.Model):
#     user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="user")

#     # Login Email Verification --------------------------------------
#     email_token = models.CharField(max_length=200, default=0)  ## For link Verification
#     is_email_verified = models.BooleanField(default=False)     ## For link Verification

#     # Forget Password------------------------------------------------
#     otp = models.IntegerField(default=0)

#     gen = (
#         ('Male', 'Male'),
#         ('Female', 'Female'),
#         ('Others', 'Others'),
#     )
#     pro_pic = models.ImageField(default='default_pic.jpg', upload_to="ProfilePic")
#     Cov_pic = models.ImageField(default='default_cover.jpg', upload_to="ProfilePic")
#     gender = models.CharField(max_length=20, choices=gen, null=True, blank=True)
#     date_of_birth = models.CharField(max_length=50, null=True, blank=True)
#     phone = models.CharField(max_length=15, null=True, blank=True)
#     address = models.TextField(max_length=200, null=True, blank=True)
#     otp = models.IntegerField(default=0000, null=True, blank=True)

#     def __str__(self):
#         return str(self.user)
