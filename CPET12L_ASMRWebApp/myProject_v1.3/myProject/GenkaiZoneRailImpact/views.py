from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.db import IntegrityError
import datetime
from .models import Accounts,FoodCatalog

# Create your views here.

def Admin(request):
    if request.method == "POST":
        food_name = request.POST.get('dishName')  # Match with form field names
        food_category = request.POST.get('dishCategory')
        food_price = request.POST.get('dishPrice')
        food_image = request.FILES.get('dishImage')  # Match with form field names
        food_description = request.POST.get('dishDescription')  # Match with form field 


        # Validate that Food_Description is not empty
        if not food_description:
            return HttpResponse("Food description cannot be empty.", status=400)
    
        # Create a new FoodCatalog instance
        food_item = FoodCatalog(
            FoodName=food_name,
            FoodCategory=food_category,
            FoodPrice=food_price,
            FoodImage=food_image,
            FoodDescription=food_description
        )
        food_item.save()

        return redirect('Admin')

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
    if request.method == 'POST':
        firstName = request.POST.get('first-name')
        lastName = request.POST.get('last-name')
        email = request.POST.get('email')
        password = request.POST.get('password')
        birthday = request.POST.get('birthday')
        contactNo = request.POST.get('contact-number')
        secQuestion = request.POST.get('sec-question')  # Correct variable name
        secAnswer = request.POST.get('sec-answer')
        secPin = request.POST.get('sec-pin')

        error_message = None
        if request.method == 'POST':
            email = request.POST.get('email')
            password = request.POST.get('password')
            confirm_password = request.POST.get('confirm-password')
        
            # Example validation for existing email
        if Accounts.objects.filter(Email=email).exists():
            error_message = 'Email is already registered.'
        
        # Check if passwords match
        elif password != confirm_password:
            error_message = 'Passwords didn’t match.'

        # If no errors, proceed to create the account
        else:
            # Registration logic here
            pass

        # Check if a custom security question was selected
        if secQuestion == 'custom':
            secQuestion = request.POST.get('custom-question')  # Use get()

        # Create a new account with the form data
        newAccount = Accounts(
            FirstName=firstName,
            LastName=lastName,
            Email=email,
            Password=password,
            Birthday=birthday,
            ContactNo=contactNo,
            Sec_Question=secQuestion,  # Correct variable name
            Sec_Answer=secAnswer,
            Sec_Pin=secPin
        )

        # Save the new account to the database
        newAccount.save()

def Register(request):
    error_message = None  # Initialize error_message to None

    if request.method == 'POST':
        firstName = request.POST.get('first-name')
        lastName = request.POST.get('last-name')
        email = request.POST.get('email')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm-password')
        birthday = request.POST.get('birthday')
        contactNo = request.POST.get('contact-number')
        secQuestion = request.POST.get('sec-question')  
        secAnswer = request.POST.get('sec-answer')
        secPin = request.POST.get('sec-pin')

        # Check if the email is already registered
        if Accounts.objects.filter(Email=email).exists():
            error_message = 'Email is already registered.'

        # Check if passwords match
        elif password != confirm_password:
            error_message = 'Passwords didn’t match.'

        # If there are no errors, create a new account
        if error_message is None:
            # Check if a custom security question was selected
            if secQuestion == 'custom':
                secQuestion = request.POST.get('custom-question')

            # Create a new account with the form data
            newAccount = Accounts(
                FirstName=firstName,
                LastName=lastName,
                Email=email,
                Password=password,
                Birthday=birthday,
                ContactNo=contactNo,
                Sec_Question=secQuestion,
                Sec_Answer=secAnswer,
                Sec_Pin=secPin
            )

            try:
                # Save the new account to the database
                newAccount.save()
                return redirect('Register')  # Redirect after successful registration
            except IntegrityError:
                error_message = 'An error occurred while saving your data.'

    # Render the registration page with the error message if any
    return render(request, 'Register.html', {'error_message': error_message})


def Verify(request):
    return render(request, 'Verify.html')

















