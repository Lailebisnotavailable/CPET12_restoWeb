from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.
def warp(request):
    return render(request, 'Home-Page.html')

def LogIn(request):
    return render(request, 'Log-In.html')

def Register(request):
    return render(request, 'Register.html')

def Profile(request):
    return render(request, 'Profile.html')

def Menu(request):
    return render(request, 'Menu.html')

def FoodDis(request):
    return render(request, 'Food-Display.html')

def Cart(request):
    return render(request, 'Cart.html')

def Cashier(request):
    return render(request, 'Cashier.html')












