from django.urls import path

from . import views

urlpatterns = [ 
    path('',views.warp,name='warp'),
    path('Home-Page',views.warp,name='warp'),
    path('LogIn',views.LogIn,name='LogIn'),
    path('Register',views.Register,name='Register'),
    path('ForgetPassword',views.ForgetPassword, name='ForgetPassword'),
    path('OTP',views.OneTimePassword,name='OTP'),
    path('ResetPassword',views.ResetPassword,name='ResetPassword'),
    path('Profile',views.Profile,name='Profile'),
    path('Menu',views.Menu,name='Menu'),
    path('FoodDis',views.FoodDis,name='FoodDis'),
    path('Cart',views.Cart,name='Cart'),
    path('Cashier',views.Cashier,name='Cashier'),
]