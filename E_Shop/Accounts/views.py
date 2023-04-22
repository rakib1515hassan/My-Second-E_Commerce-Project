from django.shortcuts import render,redirect


# Create your views here.
def login(request):
    return render(request, "Auth/login.html")


def registration(request):
    return render(request, "Auth/registration.html")
