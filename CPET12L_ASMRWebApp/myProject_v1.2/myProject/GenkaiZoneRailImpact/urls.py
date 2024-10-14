from django.urls import path

from . import views

urlpatterns = [
    path('Admin',views.Admin,name='Admin'),
    path('Cart',views.Cart,name='Cart'),
    path('Cashier',views.Cashier,name='Cashier'),
    path('Checkout',views.Checkout,name='Checkout'),
    path('FoodDis',views.FoodDis,name='FoodDis'),
    path('ForgetPass',views.ForgetPass,name='ForgetPass'), 
    path('',views.warp,name='warp'),
    path('Home-Page',views.warp,name='warp'),
    path('LogIn',views.LogIn,name='LogIn'),
    path('Menu',views.Menu,name='Menu'),
    path('NewPass',views.NewPass,name='NewPass'),
    path('Payment',views.Payment,name='Payment'),
    path('Profile',views.Profile,name='Profile'),
    path('Register',views.Register,name='Register'),
    path('Verify',views.Verify,name='Verify'),
]