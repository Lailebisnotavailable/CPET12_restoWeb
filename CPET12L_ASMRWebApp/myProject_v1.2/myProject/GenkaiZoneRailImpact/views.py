from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.
def Admin(request):
    return render(request, 'Admin.html')
def Cart(request):
    return render(request, 'Cart.html')

def Cashier(request):
    return render(request, 'Cashier.html')

def Checkout(request):
    return render(request, 'Checkout.html')

def FoodDis(request):
    return render(request, 'Food-Display.html')

def ForgetPass(request):
    return render(request, 'ForgetPass.html')

def warp(request):
    return render(request, 'Home-Page.html')

def LogIn(request):
    return render(request, 'Log-In.html')

def Menu(request):
    return render(request, 'Menu.html')

def NewPass(request):
    return render(request, 'NewPassword.html')

def Payment(request):
    return render(request,'PaymentViewer.html')

def Profile(request):
    return render(request, 'Profile.html')

def Register(request):
    return render(request, 'Register.html')

def Verify(request):
    return render(request, 'Verify.html')

















