import smtplib
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.db import IntegrityError
from django.db.models import Q
from .models import Accounts,FoodCatalog, Cart
from django.utils.encoding import force_str
from django.contrib.auth import logout
from django.core.paginator import Paginator
from django.contrib.auth.hashers import make_password
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib import messages
from django.core.exceptions import ValidationError
from .models import TopUp, Accounts
from django.core.files.storage import FileSystemStorage
from django.utils import timezone
from django.conf import settings
from .models import TopUp, Accounts
from .models import FoodCatalog
import json
from django.utils.timezone import now
from GenkaiZoneRailImpact.models import Accounts
from datetime import timedelta
from django.db.models import Sum
# Eto mga inadd ko pre for email to change pass
from email.mime.text import MIMEText
import smtplib
from django.urls import reverse
from django.utils.http import urlsafe_base64_decode
from email.mime.multipart import MIMEMultipart
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.contrib.auth.tokens import default_token_generator
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes
from smtplib import SMTPException, SMTP
from django.core.mail import send_mail
from django.template.loader import render_to_string
from weasyprint import HTML
from io import BytesIO
from datetime import datetime
import smtplib
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.db import IntegrityError
from django.db.models import Q
from django.db import models
from .models import Accounts, FoodCatalog, Cart, CashierApplication, TopUp, Checkout
from django.contrib.auth import logout
from django.core.paginator import Paginator
from django.contrib.auth.hashers import make_password, check_password
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib import messages
from django.core.exceptions import ValidationError
from django.core.files.storage import FileSystemStorage
from django.utils import timezone
from django.conf import settings
import json
from django.utils.timezone import now
from datetime import timedelta
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from django.urls import reverse
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.contrib.auth.tokens import default_token_generator
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes
from smtplib import SMTPException
from decimal import Decimal
from collections import defaultdict
import re
# Create your views here.

@csrf_exempt  # Allow CSRF exemption for AJAX requests, but consider using proper CSRF protection in production.
def save_cart(request):
    if request.method == 'POST':
        data = json.loads(request.body)  # Parse the incoming JSON data
        cart_data = data.get('cart', [])  # Get the cart array

        # Loop through the cart data and either create or update each cart item
        for item in cart_data:
            cart_item_id = item['id']
            quantity = item['quantity']
            
            # Check if the cart item already exists for the user (optional)
            # If it exists, update the quantity, otherwise create a new item
            cart_item, created = Cart.objects.update_or_create(
                cart_item_id=cart_item_id,
                defaults={'quantity': quantity}
            )

        return JsonResponse({'message': 'Cart saved successfully'})

    return JsonResponse({'error': 'Invalid method'}, status=405)
#####NEWNEWEKNWENWKWENWEKNSDKASD

@csrf_exempt
def change_tag_notreceive(request):
    if request.method == "POST":
        user_id = request.session.get('user_id')
        if not user_id:
            return redirect('Log-In')  # Redirect to login if user is not logged in

        data = json.loads(request.body)
        orderID = data.get('variable')
        print(orderID)
        # Fetch all checkout items that match the order ID for the logged-in user
        checkout_items = Checkout.objects.filter(AccountID=user_id, OrderID=orderID)
        
        # Perform a bulk update to set all of the filtered checkout items' status to "Received"
        checkout_items.update(Status="NotReceived")
        
        return JsonResponse({"status": "success", "order_id": orderID})
    
    return JsonResponse({"status": "error"}, status=400)

@csrf_exempt
def change_tag_standby(request):
    if request.method == "POST":
        data = json.loads(request.body)
        orderID = data.get('variable')
        customer = data.get('value')
        match = re.search(r'\(ID:\s*(\d+)\)', customer)
        if match:
            number = match.group(1)  # Extract the matched number


        # Fetch all checkout items that match the order ID for the logged-in user
        checkout_items = Checkout.objects.filter(AccountID=number, OrderID=orderID)

        # Perform a bulk update to set all of the filtered checkout items' status to "Received"
        checkout_items.update(Status="StandBy")
        
        return JsonResponse({"status": "success", "order_id": orderID})
    
    return JsonResponse({"status": "error"}, status=400)

@csrf_exempt
def change_tag_refund(request):
    if request.method == "POST":
        data = json.loads(request.body)
        orderID = data.get('variable')
        customer = data.get('value')
        match = re.search(r'\(ID:\s*(\d+)\)', customer)
        if match:
            number = match.group(1)  # Extract the matched number


        # Fetch all checkout items that match the order ID for the logged-in user
        checkout_items = Checkout.objects.filter(AccountID=number, OrderID=orderID)
        total_price = 0
        for item in checkout_items:
            total_price += item.FoodID.FoodPrice * item.Quantity
        print(total_price)
        customers_data = Accounts.objects.get(AccountID=number)
        print(customers_data.Wallet)
        customers_data.Wallet += total_price
        customers_data.save()
        print(customers_data.Wallet)
        # Perform a bulk update to set all of the filtered checkout items' status to "Received"
        checkout_items.update(Status="Refunded")
        
        return JsonResponse({"status": "success", "order_id": orderID})
    
    return JsonResponse({"status": "error"}, status=400)

def goto_receive(request):
    user_id = request.session.get('user_id')
    if not user_id:
        return redirect('Log-In')  # Redirect to login if user is not logged in

#If user is found in session, retrieve their details
    user = Accounts.objects.filter(AccountID=user_id).first()

#Retrieve the user's checkout content with status 'Standby'
    user_checkout_content = Checkout.objects.filter(AccountID=user_id, Status='Standby')

#Create a defaultdict to group items by OrderID
    grouped_orders = defaultdict(list)

#Group items by OrderID and compile food names
    for item in user_checkout_content:
        # Append the food name to the respective OrderID group
        grouped_orders[item.OrderID].append(item.FoodID.FoodName)

#Prepare the compiled data for rendering
    compiled_orders = []
    for order_id, foods in grouped_orders.items():
        compiled_food_names = ", ".join(foods)  # Join all food names into a single string
        compiled_orders.append({
            "OrderID": order_id,
            "OrderedFood": compiled_food_names,
            "Status": "Standby"  # Adjust as per the actual status
        })
    context = {
        'checkout_contents': compiled_orders,  # Pass the compiled orders
        'user_id': user.AccountID,
        'first_name': user.FirstName,
        'last_name': user.LastName,
        'user_wallet_content': user.Wallet
    }

#Render the food display page with the context
    return render(request, 'ToReceive.html', context)
####WIWIWIWIWWIWIWWWWWWWWWWWWWWWWWWWWWWWWIIIIIIIIIIIIIIIIIIIIIIIIIIIII\
####WIWIWIWIWWIWIWWWWWWWWWWWWWWWWWWWWWWWWIIIIIIIIIIIIIIIIIIIIIIIIIIIII\
@csrf_exempt
def update_quantity_value(request):
    if request.method == "POST":
        data = json.loads(request.body)
        print(data)
        item_id = data.get('variable')
        quantity = data.get('value')

        cart_item = Cart.objects.get(CartID=item_id)
        cart_item.Quantity = quantity
        cart_item.save()

        return JsonResponse({"status": "success", "item_id": item_id, "quantity": quantity})
    print("ONO BUG??")
    return JsonResponse({"status": "error"}, status=400)

def update_user_cart(request):
    print("FIREDSDANFDHAXKCHXKAFJAHSD")
    if request.method == 'POST':
        print("POSTTTTTTTTTTTTTTTTTTTTTTTT")
        try:
            # Extract data from the request
            data = json.loads(request.body)
            item_id = data.get('cart_id')
            print("CHECCEKCKCKECKECKE")
            print(item_id)
            user_id = request.session.get('user_id')  # Assuming the user ID is stored in session

            if not user_id:
                print('oops4')
                return JsonResponse({'status': 'error', 'message': 'User not logged in'}, status=400)

            # Ensure the item belongs to the logged-in user
            item = Cart.objects.filter(CartID=item_id, AccountID=user_id).first()  # Filter by item ID and user ID
            if item:
                print("GOES HERE??")
                item.delete()  # Remove the item from the cart
                return JsonResponse({'status': 'success', 'message': 'Item removed from cart'})
            else:
                print("oops3")
                return JsonResponse({'status': 'error', 'message': 'Item not found in your cart'}, status=404)
                
        except Exception as e:
            print("oops2")
            return JsonResponse({'status': 'error', 'message': str(e)}, status=500)
    print("oops")
    return JsonResponse({'status': 'error', 'message': 'Invalid request method'}, status=400)

def generate_reset_token(email):
    try:
        # Replace `Accounts` with the name of your user table
        user = Accounts.objects.get(Email=email)
        print(f"User found for email {email}: {user}")
        
        uid = urlsafe_base64_encode(force_bytes(user.AccountID))  # Replace `id` with the unique identifier in your table
        token = default_token_generator.make_token(user)
        
        print(f"Generated UID: {uid}, Token: {token}")
        return uid, token
    except Accounts.DoesNotExist:
        print(f"No user found with email: {email}")
        return None, None

#working (pero yung pag-gegenerate ng link prolly not working)
import random
from django.utils.timezone import now

def ForgetPass(request):
    if request.method == 'POST':
        email = request.POST.get('email')

        # Check if the email exists in the database
        try:
            user = Accounts.objects.get(Email=email)
        except Accounts.DoesNotExist:
            return render(request, 'ForgetPass.html', {'error': 'Email not found.'})

        # Generate OTP
        otp = random.randint(100000, 999999)  # Generate a 6-digit OTP
        user.otp = otp  # Store OTP in the user's record
        user.otp_created_at = now()  # Save the timestamp for OTP expiration
        user.save()

        # Send OTP email
        subject = "Your Password Reset OTP"
        body = f"""
        <html>
            <head>
                <style>
                    body {{
                        font-family: Arial, sans-serif;
                        background-color: #f4f4f9;
                        margin: 0;
                        padding: 0;
                    }}
                    .container {{
                        width: 100%;
                        padding: 20px;
                        background-color: #ffffff;
                        margin: 0 auto;
                        max-width: 600px;
                        border-radius: 8px;
                        box-shadow: 0px 4px 10px rgba(0, 0, 0, 0.1);
                    }}
                    .header {{
                        background-color: #4CAF50;
                        padding: 20px;
                        color: white;
                        text-align: center;
                        border-radius: 8px 8px 0 0;
                    }}
                    .content {{
                        padding: 20px;
                        color: #333333;
                        font-size: 16px;
                        line-height: 1.6;
                    }}
                    .otp-code {{
                        font-size: 24px;
                        font-weight: bold;
                        color: #4CAF50;
                        text-align: center;
                        padding: 15px;
                        background-color: #f0f8ff;
                        border: 2px solid #4CAF50;
                        border-radius: 5px;
                    }}
                    .footer {{
                        padding: 15px;
                        background-color: #f4f4f9;
                        text-align: center;
                        font-size: 12px;
                        color: #777777;
                        border-radius: 0 0 8px 8px;
                    }}
                    .button {{
                        display: inline-block;
                        padding: 12px 25px;
                        background-color: #4CAF50;
                        color: white;
                        text-decoration: none;
                        font-size: 16px;
                        border-radius: 5px;
                        margin-top: 15px;
                        text-align: center;
                    }}
                    .button:hover {{
                        background-color: #45a049;
                    }}
                </style>
            </head>
            <body>
                <div class="container">
                    <div class="header">
                        <h1>Password Reset OTP</h1>
                    </div>
                    <div class="content">
                        <p>Hello {user.FirstName},</p>
                        <p>Your OTP for password reset is:</p>
                        <div class="otp-code">
                            {otp}
                        </div>
                        <p>Please use this code to verify your identity and reset your password.</p>
                        <p>If you did not request this, please ignore this email.</p>
                        <p>Regards,<br>ASMR Ordering System</p>
                    </div>
                    <div class="footer">
                        <p>&copy; 2024 ASMR Ordering System</p>
                    </div>
                </div>
            </body>
        </html>
        """

        sender_email = settings.EMAIL_HOST_USER
        try:
            # Attach the email body and send the OTP email
            send_mail(subject, '', sender_email, [email], html_message=body)
            messages.success(request, 'An OTP has been sent to your email. Please verify to proceed.')
            return redirect('verify_otp')  # Redirect to Verify OTP view
        except Exception as e:
            # Handle any errors related to sending the email
            return render(request, 'ForgetPass.html', {'error': f"Failed to send email. Error: {str(e)}"})

    return render(request, 'ForgetPass.html')

def VerifyOTP(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        otp = request.POST.get('otp')

        try:
            user = Accounts.objects.get(Email=email)
            otp_valid_duration = timedelta(minutes=10)  # OTP valid for 10 minutes
            if user.otp == int(otp) and now() - user.otp_created_at <= otp_valid_duration:
                # OTP is valid, pass the AccountID to reset the password
                return redirect('reset_password', account_id=user.AccountID)  # Pass AccountID to the reset password view
            else:
                return render(request, 'VerifyOTP.html', {'error': 'Invalid or expired OTP.'})
        except Accounts.DoesNotExist:
            return render(request, 'VerifyOTP.html', {'error': 'Email not found.'})

    return render(request, 'VerifyOTP.html')


#working
def ResetPassword(request, account_id):
    if request.method == 'POST':
        new_password = request.POST.get('new_password')
        confirm_password = request.POST.get('confirm_password')

        # Validate the password inputs
        if new_password != confirm_password:
            return render(request, 'resetpassword.html', {'error': 'Passwords do not match.'})

        try:
            # Fetch the user by their AccountID
            user = Accounts.objects.get(AccountID=account_id)

            # Update the user's password (plain text password)
            user.Password = new_password  # Save password as plain text
            user.otp = None  # Clear OTP after reset
            user.otp_created_at = None  # Clear OTP timestamp
            user.save()  # Save changes

            # Redirect to login with success message
            messages.success(request, 'Your password has been reset successfully. Please log in.')
            return redirect('Log-In')  # Redirect to the login view

        except Accounts.DoesNotExist:
            # If the user doesn't exist, show an error
            return render(request, 'resetpassword.html', {'error': 'User not found.'})

    # Render the password reset form
    return render(request, 'resetpassword.html', {'account_id': account_id})
          

def Admin(request): 
    # Check if user is authenticated (i.e., session exists)
    user_id = request.session.get('user_id')
    account_type = request.session.get('AccountType')
    first_name = request.session.get('FirstName')
    last_name = request.session.get('LastName')

    print("Session set:", request.session.get('user_id'), request.session.get('AccountType'), request.session.get('FirstName'), request.session.get('LastName'))

    # If session is not valid, force logout and redirect to login page
    if not user_id and account_type !=Admin :
        print('naglogin pero di pinapasok')
        # Clear the session and redirect to login page
        request.session.flush()
        return redirect('Log-In')  # Replace with your actual login URL name

    # Set context for logged-in user
    context = {
        'user_id': user_id,
        'account_type' : account_type,
        'first_name': first_name,
        'last_name': last_name,
    }

    # Handle POST request (Dish add/edit logic)
    if request.method == "POST":
        dish_id = request.POST.get('dishId')
        if dish_id:
            try:
                food_item = FoodCatalog.objects.get(id=dish_id)
                food_item.FoodName = request.POST.get('dishName')
                food_item.FoodCategory = request.POST.get('dishCategory')
                food_item.FoodPrice = request.POST.get('dishPrice')
                food_item.FoodDescription = request.POST.get('dishDescription')

                food_image = request.FILES.get('dishImage')
                if food_image:
                    food_item.FoodImage = food_image
                food_item.save()
# messages cccccccccccccccccccccccccccccccccccccccccccccccccccc
                messages.success(request, "Food has been added to restaurant")
                
            except IntegrityError:
                messages.warning(request, "Food is already in the restaurant menu.")
# messages cccccccccccccccccccccccccccccccccccccccccccccccccccc

        else:
            food_name = request.POST.get('dishName')
            food_category = request.POST.get('dishCategory')
            food_price = request.POST.get('dishPrice')
            food_image = request.FILES.get('dishImage')
            food_description = request.POST.get('dishDescription')
# messages cccccccccccccccccccccccccccccccccccccccccccccccccccc
            if not food_description:
                return HttpResponse("Food description cannot be empty.", status=400)

            if FoodCatalog.objects.filter(Q(FoodName__iexact=food_name)).exists():
                messages.warning(request, "Food is already in the restaurant menu.")
# messages cccccccccccccccccccccccccccccccccccccccccccccccccccc
            food_item = FoodCatalog(
                FoodName=food_name,
                FoodCategory=food_category,
                FoodPrice=food_price,
                FoodImage=food_image,
                FoodDescription=food_description
            )
            try:
                food_item.save()
            
            except IntegrityError:
                pass

        return redirect('Admin')

    # Fetch food items for the dish list
    food_items = FoodCatalog.objects.all()
    paginator = Paginator(food_items, 5)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    # Fetch cashier applications
    cashier_applications = CashierApplication.objects.all()

    # Add additional context for the template
    context.update({
        'page_obj': page_obj,
        'cashier_applications': cashier_applications,
    })

    # Render the template with context
    return render(request, 'Admin.html', context)
#Add dish messages ccccccccccccccccc
def Cart_Bag(request):

    # Check if the user is logged in by looking for 'user_id' in the session
    user_id = request.session.get('user_id')
    if not user_id:
        return redirect('Log-In')  # Redirect to login if user is not logged in

    # Retrieve the logged-in user's data
    user = Accounts.objects.get(AccountID=user_id)
    user_cart_content = Cart.objects.filter(AccountID=user_id)


    context = {
        'users_id' : user.AccountID,
        'user_cart_content' : user_cart_content,
        'first_name': user.FirstName,
        'last_name': user.LastName,
        'user_wallet_content': user.Wallet,
    }

    return render(request, 'Cart.html', context)
 

def add_to_cart(request):
    if request.method == 'POST':
        # Retrieve data from the request (POST data from AJAX call)
        data = json.loads(request.body)
        food_id = data.get('food_id')
        user_id = data.get('user_id')
        foodinstance = FoodCatalog.objects.get(FoodId=food_id)
        userinstance = Accounts.objects.get(AccountID=user_id)
        # Check if the user is logged in
        user = Accounts.objects.filter(AccountID=user_id).first()
        if not user:
            return JsonResponse({'error': 'User not logged in'}, status=400)

        # Check if the food item is already in the user's cart
        cart_item = Cart.objects.filter(AccountID=userinstance, FoodID=foodinstance).first()

        if cart_item:
            # If the item exists, increment the quantity
            cart_item.Quantity += 1
            cart_item.save()
            return JsonResponse({'exists': True, 'message': 'Item quantity incremented.'})
        else:
            # If the item doesn't exist, create a new cart item
            Cart.objects.create(AccountID=userinstance, FoodID=foodinstance, Quantity=1)
            return JsonResponse({'exists': False, 'message': 'Item added to cart.'})

    return JsonResponse({'error': 'Invalid request method.'}, status=400)

def Cashier(request):
    # Check if user is authenticated (i.e., session exists)
    user_id = request.session.get('user_id')
    account_type = request.session.get('AccountType')
    first_name = request.session.get('FirstName')
    last_name = request.session.get('LastName')

    user_checkout_content = Checkout.objects.filter(Status='NotReceived')
    if not user_checkout_content:
        context = {
        'user_id': user_id,
        'account_type' : account_type,
        'first_name': first_name,
        'last_name': last_name,
    }
        return render(request, 'Cashier.html', context)


    
    # Create a defaultdict to group items by OrderID
    users = []
    user_idx = 0
    grouped_orders = defaultdict(list)
    first_iteration = list(user_checkout_content)[0]
    first_iteration_user = first_iteration.AccountID
    users.append(first_iteration_user)
    
    # Group items by OrderID and compile food names
    for item in user_checkout_content:
        if item.AccountID == first_iteration_user: #compare current acc id with last acc id
            # Append the food name to the respective OrderID group
            grouped_orders[item.OrderID].append(item.FoodID.FoodName)   
        else:
            first_iteration_user = item.AccountID
            users.append(first_iteration_user)
            grouped_orders[item.OrderID].append(item.FoodID.FoodName)

    # Prepare the compiled data for rendering
    compiled_orders = []
    for order_id, foods in grouped_orders.items():
        compiled_food_names = ", ".join(foods)  # Join all food names into a single string
        compiled_orders.append({
            "AccountID" : users[user_idx],
            "OrderID": order_id,
            "OrderedFood": compiled_food_names,
            "Status": 'NotReceived'  # Adjust as per the actual status
        })

        if user_idx < len(users) - 1:
            user_idx += 1
    

    # If session is not valid, force logout and redirect to login page
    if not user_id :
        print('naglogin pero di pinapasok')
        # Clear the session and redirect to login page
        request.session.flush()
        return redirect('Log-In')  # Replace with your actual login URL name

    # Set context for logged-in user
    context = {
        'checkout_contents' : compiled_orders,
        'user_id': user_id,
        'account_type' : account_type,
        'first_name': first_name,
        'last_name': last_name,
    }
    return render(request, 'Cashier.html', context)

#send email notif for order confirm
def GoCheckout(request):
    user_id = request.session.get('user_id')
    if not user_id:
        return redirect('Log-In')  # Redirect to login if user is not logged in

    # Retrieve the logged-in user's data
    try:
        user = Accounts.objects.get(AccountID=user_id)
    except Accounts.DoesNotExist:
        messages.error(request, "User not found.")
        return redirect('Log-In')  # Redirect if user is not found in the database

    # Retrieve address information
    block_lot = user.BlockLot if user.BlockLot != "None" else ""
    street = user.Street if user.Street != "None" else ""
    subdivision = user.Subdivision if user.Subdivision != "None" else ""
    barangay = user.Barangay if user.Barangay != "None" else ""
    city = user.City if user.City != "None" else ""
    province = user.Province if user.Province != "None" else ""

    # Check if form is submitted (check if POST request)
    if request.method == "POST":
        # Compose the order confirmation email in HTML
        subject = "Order Confirmation"
        body = f"""
        <html>
            <body style="font-family: Arial, sans-serif; background-color: #f8f8f8; color: #333;">
                <div style="max-width: 600px; margin: auto; background-color: #ffffff; padding: 20px; border-radius: 8px;">
                    <h2 style="text-align: center; color: #FF7866;">Order Confirmation</h2>
                    <p>Hello {user.FirstName} {user.LastName},</p>
                    <p>Thank you for your order! We are processing it now. Here are the details:</p>
                    
                    <h3>Delivery Address:</h3>
                    <p><strong>Block/Lot:</strong> {block_lot}</p>
                    <p><strong>Street:</strong> {street}</p>
                    <p><strong>Subdivision:</strong> {subdivision}</p>
                    <p><strong>Barangay:</strong> {barangay}</p>
                    <p><strong>City:</strong> {city}</p>
                    <p><strong>Province:</strong> {province}</p>

                    <h3>Order Summary:</h3>
                    <p>Your order is being processed.</p>

                    <p style="text-align: center; font-size: 12px; color: #888;">&copy; 2024 ASMR Restaurant Ordering System</p>
                </div>
            </body>
        </html>
        """
        sender_email = settings.EMAIL_HOST_USER

        try:
            msg = MIMEMultipart()
            msg['From'] = sender_email
            msg['To'] = user.Email
            msg['Subject'] = subject
            msg.attach(MIMEText(body, 'html'))

            # Sending email using SMTP
            with SMTP("smtp.gmail.com", 587) as server:
                server.starttls()
                server.login(sender_email, settings.EMAIL_HOST_PASSWORD)
                server.sendmail(sender_email, user.Email, msg.as_string())

            messages.success(request, "Confirmation email sent successfully.")
        except Exception as e:
            messages.error(request, f"Failed to send email: {e}")

    # Add these values to the context for rendering Checkout page
    context = {
        'first_name': user.FirstName,
        'last_name': user.LastName,
        'user_wallet_content': user.Wallet,
        'block_lot': block_lot,
        'street': street,
        'subdivision': subdivision,
        'barangay': barangay,
        'city': city,
        'province': province,
    }

    return render(request, 'Checkout.html', context)

def GotoCheckout(request):
    user_id = request.session.get('user_id')
    if not user_id:
        return redirect('Log-In')  # Redirect to login if user is not logged in

    # Retrieve the logged-in user's data
    user = Accounts.objects.get(AccountID=user_id)
    user_cart_content = Cart.objects.filter(AccountID=user_id)
    block_lot = user.BlockLot if user.BlockLot != "None" else ""
    street = user.Street if user.Street != "None" else ""
    subdivision = user.Subdivision if user.Subdivision != "None" else ""
    barangay = user.Barangay if user.Barangay != "None" else ""
    city = user.City if user.City != "None" else ""
    province = user.Province if user.Province != "None" else ""

    # Add these values to the context
    context = {
    'user_cart_content' : user_cart_content,
    'first_name': user.FirstName,
    'last_name': user.LastName,
    'user_wallet_content': user.Wallet,
    'block_lot': block_lot,
    'street': street,
    'subdivision': subdivision,
    'barangay': barangay,
    'city': city,
    'province': province,
    }

    return render(request, 'Checkout.html', context)

def HandleCheckout(request):
    print("Processing checkout...")
    if request.method == 'POST':
        user_id = request.session.get('user_id')
        print(user_id)
        if not user_id:
            return redirect('Log-In')  # Redirect to login if user is not logged in
        user = Accounts.objects.get(AccountID=user_id)  # Get user by ID
        cart_data = json.loads(request.POST.get("cart_data"))
        total_price = float(request.POST.get("total_price"))
        user_balance = float(request.POST.get("user_balance"))
        print(user.Wallet)
        deduction = user_balance - total_price
        user.Wallet = deduction
        user.save()

        # Generate unique order ID
        FoundUniqueId = False
        uniquekey = 0
        while not FoundUniqueId:
            check = Checkout.objects.filter(AccountID=user_id, OrderID=uniquekey).exists()
            print(check)
            if not check:
                FoundUniqueId = True
            else:
                uniquekey += 1
        print(f"UniqueKey for this order is: {uniquekey}")

        # Save each ordered food to the database
        for items in cart_data:
            food_id = items.get("foodId")
            print(f"Processing food ID: {food_id}")
            mismongfood = FoodCatalog.objects.get(FoodId=food_id)
            food_quantity = items.get("quantity")
            ordered_food = Checkout(AccountID=user, FoodID=mismongfood, Quantity=food_quantity, OrderID=uniquekey)
            ordered_food.save()

        # Empty the user's cart
        users_cart_content = Cart.objects.filter(AccountID=user.AccountID)
        users_cart_content.delete()

        # Sending order confirmation email
        subject = "Order Confirmation"
        body = f"""
        <html>
            <body style="font-family: Arial, sans-serif; background-color: #f8f8f8; color: #333;">
                <div style="max-width: 600px; margin: auto; background-color: #ffffff; padding: 20px; border-radius: 8px;">
                    <h2 style="text-align: center; color: #FF7866;">Order Confirmation</h2>
                    <p>Hello {user.FirstName} {user.LastName},</p>
                    <p>Thank you for your order! We are processing it now. Here are the details:</p>
                    
                    <h3>Delivery Address:</h3>
                    <p><strong>Block/Lot:</strong> {user.BlockLot if user.BlockLot != "None" else ""}</p>
                    <p><strong>Street:</strong> {user.Street if user.Street != "None" else ""}</p>
                    <p><strong>Subdivision:</strong> {user.Subdivision if user.Subdivision != "None" else ""}</p>
                    <p><strong>Barangay:</strong> {user.Barangay if user.Barangay != "None" else ""}</p>
                    <p><strong>City:</strong> {user.City if user.City != "None" else ""}</p>
                    <p><strong>Province:</strong> {user.Province if user.Province != "None" else ""}</p>

                    <h3>Order Details:</h3>
                    <ul style="list-style: none; padding: 0;">
        """

        for item in Checkout.objects.filter(AccountID=user_id, OrderID=uniquekey):
            food_name = item.FoodID.FoodName
            quantity = item.Quantity
            body += f"<li>{food_name} x {quantity}</li>"

        body += """
                    </ul>
                    <p>Your order is being processed.</p>

                    <p style="text-align: center; font-size: 12px; color: #888;">&copy; 2024 ASMR Restaurant Ordering System</p>
                </div>
            </body>
        </html>
        """
        sender_email = settings.EMAIL_HOST_USER

        try:
            msg = MIMEMultipart()
            msg['From'] = sender_email
            msg['To'] = user.Email
            msg['Subject'] = subject
            msg.attach(MIMEText(body, 'html'))

            # Sending email using SMTP
            with SMTP("smtp.gmail.com", 587) as server:
                server.starttls()
                server.login(sender_email, settings.EMAIL_HOST_PASSWORD)
                server.sendmail(sender_email, user.Email, msg.as_string())

            messages.success(request, "Confirmation email sent successfully.")
        except Exception as e:
            messages.error(request, f"Failed to send email: {e}")

        # Redirect to Done.html after successful checkout
        return redirect('Done')

    return redirect('Log-In')  # If the request method is not POST, redirect to login




def done_view(request):
    if request.method == "POST":
        # Here you would handle sending an email to the user
        # Example: Sending an email
        subject = "Order Confirmation"
        message = "Thank you for ordering using our app!"
        recipient_list = [request.session.get('user_email')]  # Assuming user_email is stored in session
        
        send_mail(
            subject,
            message,
            settings.DEFAULT_FROM_EMAIL,
            recipient_list,
            fail_silently=False,
        )
        
        # Redirect to the menu or confirmation page
        return redirect('Menu')  # Update with your actual menu URL

    return render(request, 'Done.html')
#for generate pdf
def generate_pdf_view(request):
    # Fetch all data from the models
    food_items = FoodCatalog.objects.all()
    checkout_info = Checkout.objects.values('Status', 'OrderID', 'Quantity')

    # Render the HTML template with context
    html_string = render_to_string('full_report_template.html', {
        'food_items': food_items,
        'checkout_info': checkout_info,
    })

    # Create a PDF object
    html = HTML(string=html_string)
    pdf_file = BytesIO()
    html.write_pdf(pdf_file)

    # Prepare the response
    response = HttpResponse(pdf_file.getvalue(), content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="ASMRCashierReport.pdf"'

    return response

def FAQs(request):
    return render(request, 'FAQs.html')

def FoodDis(request, FoodId):
    # Retrieve food details via FoodId
    food_item = get_object_or_404(FoodCatalog, FoodId=FoodId)
    ##NEWWWWWWWWWWWWWWWWWWWWWWWK:INEENDANSKDAJSDLINENEINEINDIASDJHLASCJAXC
    food_item.FoodViews += 1
    ##HASJDWWOOOOOOOWOWOASHDAJSDWOWOWOWOWO!!WDASDKWWOWO!
    food_item.save()
    print("SHUULD SAVE NOWW SAHJKDASKJCHXXKCXHASCKL")
    # Retrieve user information if available
    user_id = request.session.get('user_id')
    
    if user_id:
        # If user is found in session, retrieve their details
        user = Accounts.objects.filter(AccountID=user_id).first()
        
        if user:
            context = {
                'user_id' : user.AccountID,
                'food_item': food_item,
                'first_name': user.FirstName,
                'last_name': user.LastName,
                'user_wallet_content': user.Wallet,
            }
        else:
            # If user is not found, treat as a guest
            context = {
                'food_item': food_item,
                'first_name': 'Guest',
                'last_name': '',
                'user_wallet_content': 0,
            }
    else:
        # If user_id is not in the session, treat as guest
        context = {
            'food_item': food_item,
            'first_name': 'Guest',
            'last_name': '',
            'user_wallet_content': 0,
        }

    # Render the food display page with the context
    return render(request, 'Food-Display.html', context)

@csrf_exempt
def change_tag_receive(request):
    if request.method == "POST":
        user_id = request.session.get('user_id')
        if not user_id:
            return redirect('Log-In')  # Redirect to login if user is not logged in

        data = json.loads(request.body)
        orderID = data.get('variable')
        
        # Fetch all checkout items that match the order ID for the logged-in user
        checkout_items = Checkout.objects.filter(AccountID=user_id, OrderID=orderID)
        
        # Perform a bulk update to set all of the filtered checkout items' status to "Received"
        checkout_items.update(Status="Received")
        
        return JsonResponse({"status": "success", "order_id": orderID})
    
    return JsonResponse({"status": "error"}, status=400)






def warp(request):
    return render(request, 'Home-Page.html',)

def LogIn(request):
    if request.method == "POST":
        email = request.POST.get('email')
        password = request.POST.get('password')
        
        if email and password:
            user = Accounts.objects.filter(Email=email, Password=password).first()
            print("User from database:", user)
            print("Entered Password:", password)
            print("Stored Password:", user.Password if user else 'None')

            if user and user.Password == password:  # Plain text comparison
                request.session['user_id'] = user.AccountID
                request.session['AccountType'] = user.AccountType
                request.session['FirstName'] = user.FirstName
                request.session['LastName'] = user.LastName

                account_type = user.AccountType
                if account_type == "Admin":
                    messages.success(request, f"You have successfully logged in, {user.FirstName} {user.LastName}!")
                    return redirect('Admin')
                elif account_type == "Cashier":
                    return redirect('Cashier')
                elif account_type == "Customer":
                    messages.success(request, f"You have successfully logged in, {user.FirstName} {user.LastName}!")
                    return redirect('Menu')
                else:
                    return render(request, 'Log-In.html', {'error_message': 'Unknown account type.'})
            else:
                return render(request, 'Log-In.html', {'error_message': 'Invalid email or password.'})
        else:
            return render(request, 'Log-In.html', {'error_message': 'Both email and password are required.'})

    return render(request, 'Log-In.html')
# Account Filtering and Redirecting cccccccccccccccccccccccccccccccccccccccccccccccccccc
# Force redirect to Profile cccccccccccccccccccccccccc
def check_profile_completion(user):
    # Define the fields that are required
    required_fields = ['Street', 'BlockLot', 'City', 'Province']
    
    # Check for null or empty fields
    for field in required_fields:
        if not getattr(user, field, None):  # If field is None or empty
            return False
    return True
# Force redirect to Profile cccccccccccccccccccccccccc

def Menu(request):
    sort_category = request.GET.get('sort', 'all')  # Get the sort parameter from the request, default to 'all'
    search_query = request.GET.get('search', '')  # Get the search query from the request

    # Fetch all food items initially
    food_items = FoodCatalog.objects.all()

    # Filter by category if 'sort' value is provided
    if sort_category and sort_category != 'all':
        food_items = food_items.filter(FoodCategory__iexact=sort_category)  # Case-insensitive match

    # Filter by search query if it's provided
    if search_query:
        food_items = food_items.filter(FoodName__icontains=search_query)  # Case-insensitive search by food name

    # Handle case where no items match the filter
    if not food_items.exists():
        food_items = None

    # Check if the user is authenticated by checking the session
    user_id = request.session.get('user_id')  # Get user ID from session

    if user_id:
        user = Accounts.objects.filter(AccountID=user_id).first()  # Fetch the user using the session user_id
# Force redirect to Profile cccccccccccccccccccccccccc
        if not check_profile_completion(user):
            messages.warning(request, "Please complete your profile information before proceeding. Check every entry if filled correctly.")
            return redirect('Profile')  # Redirect to profile page
# Force redirect to Profile cccccccccccccccccccccccccc

        if user:
            context = {
                'food_items': food_items,
                'first_name': user.FirstName,
                'last_name': user.LastName,
                'user_wallet_content': user.Wallet,  # Assuming Wallet is a field in the Accounts model
                'user': user,  # Include user object for profile image and other details
                'page_title': 'Menu',  # Title for the page
            }
        else:
            # If user not found, set default context for guest
            context = {
                'food_items': food_items,
                'first_name': 'Guest',
                'last_name': '',
                'user_wallet_content': 0,
                'user': None,
                'page_title': 'Menu',
            }
    else:
        # If user_id is not found in the session, treat as guest
        context = {
            'food_items': food_items,
            'first_name': 'Guest',
            'last_name': '',
            'user_wallet_content': 0,
            'user': None,
            'page_title': 'Menu',
        }

    # Render the menu page with the context
    return render(request, 'Menu.html', context)
# Force redirect to Profile cccccccccccccccccccccccccc



def Profile(request):
    user_id = request.session.get('user_id')  # Get user ID from session
    user_checkout_content = Checkout.objects.filter(AccountID=user_id, Status='Received')
    
    # Create a defaultdict to group items by OrderID
    grouped_orders = defaultdict(list)
    
    # Group items by OrderID and compile food names
    for item in user_checkout_content:
        # Append the food name to the respective OrderID group
        grouped_orders[item.OrderID].append(item.FoodID.FoodName)

    # Prepare the compiled data for rendering
    compiled_orders = []
    for order_id, foods in grouped_orders.items():
        compiled_food_names = ", ".join(foods)  # Join all food names into a single string
        compiled_orders.append({
            "OrderID": order_id,
            "OrderedFood": compiled_food_names,
            "Status": "Standby"  # Adjust as per the actual status
        })

    if user_id:
        user = Accounts.objects.filter(AccountID=user_id).first()  # Fetch the user
        if user:
            # Prepare context variables for the greeting
            context = {
                'checkout_contents': compiled_orders,
                'first_name': user.FirstName,
                'last_name': user.LastName,
                'user_wallet_content': user.Wallet,
                'user': user,  # Include user object for profile image and other details
                'page_title': 'Profile',
            }
            print(context)  # Debugging: Check if context is populated correctly

            if request.method == 'POST':
                if 'profile-image' in request.FILES:
                    profile_image = request.FILES['profile-image']
                    user.ProfileImage.save(profile_image.name, profile_image)  # Save the uploaded image

                # Update user profile
                user.FirstName = request.POST.get('first-name')
                user.LastName = request.POST.get('last-name')
                user.ContactNo = request.POST.get('contact-no')
                user.Email = request.POST.get('email')
                user.BlockLot = request.POST.get('block-lot')
                user.Street = request.POST.get('street')
                user.Subdivision = request.POST.get('subdivision')
                user.Barangay = request.POST.get('barangay')
                user.City = request.POST.get('city')
                user.Province = request.POST.get('province')
                # Handle password update logic if needed (be sure to hash it!)
                user.save()  # Save updated user information
                return redirect('Profile') 
            
            # Render the profile template with the context
            return render(request, 'Profile.html', context)  
        else:
            print("User not found.")  # Debugging: Check if user retrieval fails
            return render(request, 'Profile.html', {'error_message': 'User not found.'})
    else:
        return redirect('Log-In')  

def Cart_Bag(request):

    # Check if the user is logged in by looking for 'user_id' in the session
    user_id = request.session.get('user_id')
    if not user_id:
        return redirect('Log-In')  # Redirect to login if user is not logged in

    # Retrieve the logged-in user's data
    user = Accounts.objects.get(AccountID=user_id)
    user_cart_content = Cart.objects.filter(AccountID=user_id)


    context = {
        'users_id' : user.AccountID,
        'user_cart_content' : user_cart_content,
        'first_name': user.FirstName,
        'last_name': user.LastName,
        'user_wallet_content': user.Wallet,
    }

    return render(request, 'Cart.html', context)

def Register(request):
    error_message = None  # Initialize error_message to None

    if request.method == 'POST':
        accountType = request.POST.get('account-type')
        firstName = request.POST.get('first-name')
        lastName = request.POST.get('last-name')
        email = request.POST.get('email')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm-password')
        birthday = request.POST.get('birthday')
        contactNo = request.POST.get('contact-number')

        # Debugging lines
        print(request.POST)
        print(f"First Name: {firstName}, Last Name: {lastName}, Email: {email}")  
        print(f"Password: {password}, Confirm Password: {confirm_password}")

        # Email Authentication
        if Accounts.objects.filter(Email=email).exists():
            error_message = 'Email is already registered.'
            print("Email already exists")  

        # Contact Number Authentication
        elif Accounts.objects.filter(ContactNo=contactNo).exists():
            error_message = 'Contact number is already registered.'
            print("Contact number already exists")  

        # Password matching
        elif password != confirm_password:
            error_message = 'Passwords didn’t match.'
            print("Passwords do not match")

        else:
            try:
                # Store plain text password instead of hashed
                if accountType == 'Cashier':
                    # Save to CashierAccounts model
                    newAccount = CashierApplication(
                        FirstName=firstName,
                        LastName=lastName,
                        Email=email,
                        Password=password,  # Store plain text password
                        Birthday=birthday,
                        ContactNo=contactNo
                    )
                    newAccount.save()

                else:  # Default to customer account
                    # Save to Accounts model
                    newAccount = Accounts(
                        AccountType=accountType,
                        FirstName=firstName,
                        LastName=lastName,
                        Email=email,
                        Password=password,  # Store plain text password
                        Birthday=birthday,
                        ContactNo=contactNo
                    )
                    newAccount.save()
                    print("Account created successfully")  # Debug line

            except IntegrityError as e:
                error_message = 'An unexpected error occurred. Please try again.'
                print(f"IntegrityError: {e}")  # Debug line

    return render(request, 'Register.html', {'error_message': error_message})

# for cashier applicant cccccccccccccccccccccccccccccccccccccccccccccccccccc
def process_application(request):
    # Check if user is authenticated (i.e., session exists)
    user_id = request.session.get('user_id')
    account_type = request.session.get('AccountType')
    first_name = request.session.get('FirstName')
    last_name = request.session.get('LastName')

    print("Session set:", request.session.get('user_id'), request.session.get('AccountID'), request.session.get('FirstName'), request.session.get('LastName'))

    # If session is not valid, force logout and redirect to login page
    if not user_id or account_type != "Admin":
        print('Unauthorized access attempt.')
        request.session.flush()
        return redirect('Log-In')  # Replace with your actual login URL name

    # Set context for logged-in user
    context = {
        'user_id': user_id,
        'account_type': account_type,
        'first_name': first_name,
        'last_name': last_name,
    }

    if request.method == "POST":
        applicant_id = request.POST.get('applicant_id')
        action = request.POST.get('action')

        try:
            application = get_object_or_404(CashierApplication, ApplicantID=applicant_id)

            if action == "approve":
                # Add the applicant to the Accounts model
                Accounts.objects.create(
                    AccountType="Cashier",
                    FirstName=application.FirstName,
                    LastName=application.LastName,
                    Email=application.Email,
                    Password=application.Password,  # Ensure the password is hashed in CashierApplication
                    Birthday=application.Birthday,
                    ContactNo=application.ContactNo,
                )
                
                # Remove the application after approval
                application.delete()
                print(f"Application for {application.FirstName} {application.LastName} approved and added to Accounts.")

            elif action == "reject":
                # Remove the application if rejected
                application.delete()
                print(f"Application for {application.FirstName} {application.LastName} rejected.")

            # Redirect to admin dashboard or appropriate page
            return redirect('Admin')

        except CashierApplication.DoesNotExist:
            return HttpResponse("Application not found.", status=404)

    return HttpResponse("Invalid request.", status=400)
# for cashier applicant cccccccccccccccccccccccccccccccccccccccccccccccccccc

def sign_out(request):
    logout(request)  # This logs out the user
    return redirect('Log-In')  # Redirect to the login page

def TopUp(request):
    # Check if the user is logged in by looking for 'user_id' in the session
    user_id = request.session.get('user_id')
    if not user_id:
        return redirect('Log-In')  # Redirect to login if user is not logged in

    # Retrieve the logged-in user's data
    user = Accounts.objects.get(AccountID=user_id)
    context = {
        'first_name': user.FirstName,
        'last_name': user.LastName,
        'user_wallet_content': user.Wallet,
    }

    return render(request, 'TopUp.html', context)

def topup_apply(request):
    if request.method == 'POST':
        user_id = request.session.get('user_id')
        if not user_id:
            return redirect('Log-In')  # Redirect to login if user is not logged in
        user = Accounts.objects.get(AccountID=user_id) #Get user id :3
        topup_amount = request.POST.get('topup-amount')
        user_balance = user.Wallet
        user_balance += Decimal(topup_amount)
        
        # Convert to integer and check if the amount is valid
        try:
            topup_amount = float(topup_amount)
            if topup_amount >= 20:
                # Update the user's wallet balance
                user.Wallet = user_balance
                user.save()

                # Respond with success and the new balance
                return JsonResponse({
                    'success': True,
                    'new_balance': user.Wallet
                })
            else:
                return JsonResponse({
                    'success': False,
                    'message': 'Minimum top-up is ₱20.'
                })

        except ValueError:
            return JsonResponse({
                'success': False,
                'message': 'Invalid amount entered.'
            })
    
    context = {
        'first_name': user.FirstName,
        'last_name': user.LastName,
        'user_wallet_content': user.Wallet,
    }

    return render(request, 'TopUp.html', context)

def Verify(request):
    return render(request, 'Verify.html') #the view function to avoid conflict with the model class
    if request.method == "POST":
        # Get form data
        topup_amount = request.POST.get("topup-amount")
        proof_file = request.FILES.get("image-upload")

        # Debugging: Print received values
        print(f"Received top-up amount: {topup_amount}")
        print(f"Received proof file: {proof_file}")

        # Validate top-up amount
        if not topup_amount or float(topup_amount) < 20:
            print("Invalid top-up amount or less than 20 pesos")
            messages.error(request, "Invalid top-up amount. Minimum is ₱20.")
            return redirect("TopUp")  # Redirect back to the top-up page

        # Use QuerySet API to save the data
        try:
            # Create and save the TopUp transaction in one step
            topup_transaction = TopUp.objects.create(
                topup_amount=float(topup_amount),  # Convert to float
                proof=proof_file,  # The file from the form
                status="pending",  # Default status
                transaction_date=timezone.now(),  # Set the current timestamp
            )
            print(f"Top-up transaction saved: {topup_transaction}")  # Print to confirm

            # Show success message
            messages.success(request, "Top-up request submitted successfully. Please wait for processing.")
        except Exception as e:
            print(f"Error: {e}")  # Catch and print any error
            messages.error(request, f"An error occurred: {e}")  # Show error message

        return redirect("TopUp")  # Redirect back to the top-up page

    # Handle GET request to render the top-up page
    return render(request, "TopUp.html")

    if request.method == 'POST':
        email = request.POST['email']
        new_password = request.POST['new_password']
        try:
            user = CustomUser.objects.get(email=email)
            user.password = make_password(new_password)  # Hash the password
            user.save()
            return render(request, 'reset_success.html')  # Success page
        except CustomUser.DoesNotExist:
            return render(request, 'NewPassword.html', {'error': 'User not found'})
    return render(request, 'NewPassword.html') 









